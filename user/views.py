from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from knox.models import AuthToken 
from .serializers import *


from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


from knox.auth import TokenAuthentication


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user=serializer.save()
        return Response({
            'token':AuthToken.objects.create(user)[1]
        })
        
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
           user = serializer.validated_data
           return Response({
               "user": UserSerializer(user,
                                      context=self.get_serializer_context()).data, 
           }) 

class UserAPI(generics.RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserSerializer
    def get_object(self):
        return self.request.user
 

#change Password
    
def changePasswordView(request):
   serializer= ChangePasswordSerializer(data=request.data)
   if serializer.is_valid():
       user = request.user
       old_password = serializer.validated_data['old_password']
       new_password = serializer.validated_data['new_password']
       
       if not user.check_password(old_password):
           return Response({"error":"your old password is incorrect"})
       
       user.set_password(new_password)
       user.save()
       return Response({"message":"password changed successfully"})
   
   return Response(serializer.errors)
        
    
    
class ResetPasswordAPI(APIView):
    serializer_class = ResetPasswordSerializer
    
    def post (self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            email = user.email
            uid = serializer.uid
            token = serializer.token
            
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string("user/reset_password_email.html", {
                'user': user,
                'domain': current_site.domain,
                'uid':uid,
                'token' : token,
            })
            to_email = email
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send()
            
            return Response ({'message':'password reset email has send'})
        
        
        return Response(serializer.errors)
    
    
    
class SetNewPasswordAPI(APIView):
    serializer_class = SetNewPasswordSerializer
    
    def post(self, request, uid, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.set_new_password(uid, token)
            if user:
                return Response({'message':'password Reset Successfull'})
            return Response({'message': 'Invalid token.'})
            
        return Response(serializer.errors)
		