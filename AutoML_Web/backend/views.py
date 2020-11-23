from django.shortcuts import render

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

import sys
sys.path.append("..")
from _app import models
# Create your views here.

# class Test(APIView):
#     def get(self, request):
#         a = request.GET['a']
#         res = {
#             'success': True,
#             'data': 'a'
#         }
#         return Response(res)
## 每个页面对应一个类?
class OverView(APIView):
    def get(self, request):
        """
        login get
        """
        pass
        return Response()
    def post(self,request):
        pass
    
class Login(APIView):
    def get(self, request):
        """
        login get
        """
        print("GET: ",type(request))
        print(request)
        # print(i for i in request)
        status={
            "status":"ok",
            "type":"account",
            "currentAuthority":"admin",
        }        
        return Response(data=status)
    def post(self,request):
        print("POST: ",type(request))
        print(request)
        # print(i for i in request)
        status={
            "status":"ok",
            "type":"account",
            "currentAuthority":"admin",
        }       
        return Response(data=status)
class currentUser(APIView):
    def get(self,request):
        pass
    def post(self, request):
        """
        post
        """
        pass
class AutoML(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class CreateMission(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class DataManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class DevEnv(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
     
class AlgoManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class TrainJobManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class AutoJobManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class ModelManage(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
    
class AIMarket(APIView):
    def get(self, request):
        """
        login get
        """
        pass
    def post(self,request):
        pass 
