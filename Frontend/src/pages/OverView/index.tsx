import React from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProCard from '@ant-design/pro-card'
import { Carousel, Card, Alert, Typography } from 'antd';
import styles from './index.less';

// import shower from '../../../public/banner1.jpg'
import mac from '../../../public/MAC.jpg'
import pcl from '../../../public/PCL.jpg'

const CodePreview: React.FC<{}> = ({ children }) => (
  <pre className={styles.pre}>
    <code>
      <Typography.Text copyable>{children}</Typography.Text>
    </code>
  </pre>
);

export default (): React.ReactNode => (
  <PageContainer>
    <Carousel autoplay >
      <div>
        <img alt="MAC" src={mac} />
      </div>
      <div>
        <img alt="PCL" src={pcl} />
      </div>
    </Carousel>
    <ProCard style={{ marginTop: 8 }} gutter={8} layout="center" title="新手入门" bordered headerBordered>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        准备工作
      </ProCard>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        获取数据
      </ProCard>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        执行引导
      </ProCard>
    </ProCard>
    <ProCard gutter={8} title="开发工具" layout="center" bordered headerBordered>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        <h1>PyCharm ToolKit</h1>
      </ProCard>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        <h1>Model SDK</h1>
      </ProCard>
      <ProCard colSpan={{ xs: 2, sm: 4, md: 6, lg: 8, xl: 10 }} layout="center" bordered>
        <h1>PCL SDK</h1>
      </ProCard>
    </ProCard>
  </PageContainer>
);
