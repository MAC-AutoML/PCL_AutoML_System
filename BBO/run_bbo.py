import logging
from BBO.space import JointSpace
import numpy as np
from time import time
from BBO.optimizer import random_search as rs
from BBO.optimizer.random_optimizer import RandomOptimizer
from BBO.test_problem import rastrigin_function,classify_train
import os


logger = logging.getLogger(__name__)

def main(optimizer, test_problem, n_calls, n_suggestions, n_obj=1):
    """Run a study for a single optimizer on a single test problem.

    This function can be used for benchmarking on general stateless objectives (not just `sklearn`).

    Parameters
    ----------
    optimizer : :class:`.abstract_optimizer.AbstractOptimizer`
        Instance of one of the wrapper optimizers.
    test_problem : :class:`.sklearn_funcs.TestFunction`
        Instance of test function to attempt to minimize.
    n_calls : int
        How many iterations of minimization to run.
    n_suggestions : int
        How many parallel evaluation we run each iteration. Must be ``>= 1``.
    n_obj : int
        Number of different objectives measured, only objective 0 is seen by optimizer. Must be ``>= 1``.

    Returns
    -------
    function_evals : :class:`numpy:numpy.ndarray` of shape (n_calls, n_suggestions, n_obj)
        Value of objective for each evaluation.
    timing_evals : (:class:`numpy:numpy.ndarray`, :class:`numpy:numpy.ndarray`, :class:`numpy:numpy.ndarray`)
        Tuple of 3 timing results: ``(suggest_time, eval_time, observe_time)`` with shapes ``(n_calls,)``,
        ``(n_calls, n_suggestions)``, and ``(n_calls,)``. These are the time to make each suggestion, the time for each
        evaluation of the objective function, and the time to make an observe call.
    suggest_log : list(list(dict(str, object)))
        Log of the suggestions corresponding to the `function_evals`.
    """
    assert n_suggestions >= 1, "batch size must be at least 1"
    assert n_obj >= 1, "Must be at least one objective"

    space_for_validate = JointSpace(test_problem.get_api_config())

    suggest_time = np.zeros(n_calls)
    observe_time = np.zeros(n_calls)
    eval_time = np.zeros((n_calls, n_suggestions))
    function_evals = np.zeros((n_calls, n_suggestions, n_obj))
    tn = [None]*n_suggestions
    print(len(tn))
    suggest_log = [tn] * n_calls
    print(len(suggest_log))
    print(len(suggest_log[0]))
    mi = 999999
    for ii in range(n_calls):
        tt = time()
        try:
            next_points = optimizer.suggest(n_suggestions)
        except Exception as e:
            logger.warning("Failure in optimizer suggest. Falling back to random search.")
            logger.exception(e, exc_info=True)
            # print(json.dumps({"optimizer_suggest_exception": {ITER: ii}}))
            api_config = test_problem.get_api_config()
            next_points = rs.suggest_dict([], [], api_config, n_suggestions=n_suggestions)
        suggest_time[ii] = time() - tt

        logger.info("suggestion time taken %f iter %d next_points %s" % (suggest_time[ii], ii, str(next_points)))
        assert len(next_points) == n_suggestions, "invalid number of suggestions provided by the optimizer"
        # logging.info("1")

        # We could put this inside the TestProblem class, but ok here for now.
        try:
            space_for_validate.validate(next_points)  # Fails if suggestions outside allowed range
        except Exception:
            raise ValueError("Optimizer suggestion is out of range.")
        m_list = [mi]
        for jj, next_point in enumerate(next_points):
            print(next_points)
            tt = time()
            try:
                f_current_eval = test_problem.evaluate(next_point,ii,jj)
                #m_list.append(f_current_eval)
                #mi = min(f_current_eval, mi)
            except Exception as e:
                logger.warning("Failure in function eval. Setting to inf.")
                logger.exception(e, exc_info=True)
                f_current_eval = np.full((n_obj,), np.inf, dtype=float)
            eval_time[ii, jj] = time() - tt
            print('epoch {},iter {}, f_current {}'.format(ii,jj, f_current_eval))
            # print('f_current shape', f_current_eval.size)

            assert f_current_eval.size == n_obj

            suggest_log[ii][jj] = next_points
            function_evals[ii, jj, :] = f_current_eval
            # logger.info(
            #     "function_evaluation time %f value %f suggestion %s"
            #     % (eval_time[ii, jj], f_current_eval[0], str(next_point))
            # )
        print(len(next_points))
        for kk in range(len(next_points)):
            _,outpath = test_problem.printinfo()
            new_outpath = outpath + "/bbo_out_" + str(ii) + "_" + str(kk)
            while True:
                if os.path.isfile(new_outpath + "/reward.txt"):
                    fp = open(new_outpath + "/reward.txt", 'r')
                    st = fp.read()
                    fp.close()
                    reward = int(st)
                    m_list.append(reward)
                    break
        mi = min(m_list)
        # logging.info("3")

        # Note: this could be inf in the event of a crash in f evaluation, the optimizer must be able to handle that.
        # Only objective 0 is seen by optimizer.
        eval_list = function_evals[ii, :, 0].tolist()


        tt = time()
        try:
            optimizer.observe(next_points, eval_list)
        except Exception as e:
            logger.warning("Failure in optimizer observe. Ignoring these observations.")
            # logger.exception(e, exc_info=True)
            # print(json.dumps({"optimizer_observe_exception": {ITER: ii}}))
        observe_time[ii] = time() - tt

        # logger.info(
        #     "observation time %f, current best %f at iter %d"
        #     % (observe_time[ii], np.min(function_evals[: ii + 1, :, 0]), ii)
        # )
    print('mi', mi)

    return function_evals, (suggest_time, eval_time, observe_time), suggest_log

if __name__ == '__main__':
    test_problem=classify_train('/userhome/test/train.py',"/userhome/test/output/")
    main(RandomOptimizer(test_problem.get_api_config()), test_problem, 100, 2, 1)
