from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
from .forms import SignUpForm, ProfileForm , LoginForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

''' DJANGO REST '''
from .serializers import BookSerializer
from rest_framework.response import Response
from .models import Profile,Book
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


@login_required
def index(request):
    return HttpResponse('Welcome to Home page ',{{ user }})

def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = User_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,  'Your account has been successfully created')
            return redirect('login')
    else:
        user_form = SignUpForm()
        profile_form  =ProfileForm()
    return render(request,'signup.html',{'user_form':user_form,
                                             'profile_form': profile_form
                                             }  )

def login(request):
    if request.method=="POST":
        login_form= LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if login_form.is_valid():
            if user:
                messages.success(request,  'successfully logged in')
            return render(request,'index.html')
        return render (request,'login.html')
    else:
        login_form=LoginForm()
        return render(request,'login.html',{'form':login_form,
                                            'error':'invalid credentials'})
@login_required
def update_profile(request):
    user= request.user
    profile=request.user.profile
    if request.method=="POST":
        form= SignUpForm(request.POST, instance=user)
        profile=ProfileForm(request.POST, instance=profile)
        if form.is_valid() and  profile.is_valid():
            form.save()
            profile.save()
        return redirect('profile.html')
    else:
        return render(request,'login.html')

''' API View '''

class BookView(APIView):
    model_class=Book
    serializer_class=BookSerializer
    permission_class=[IsAuthenticated,]
    def post(self,request):
        try:
            serializer= self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': True,
                                 'message': ' book details added successfully',
                                 'data': serializer.data})
        except self.model_class.DoesNotExist:
            return Response(" No such Book Found")


    def get(self,request):
        try:
            books= self.model_class.objects.all()
            serializer= self.serializer_class(books, many=True)
            return Response({'status':True,
                             'all_books': serializer.data})

        except model_class.DoesNotExist:
            return Response(" No such Book Found")


class BookUpdateView(APIView):
    permission_class=[IsAuthenticated]
    model_class=Book
    serializer_class=BookSerializer

    def get_obj(self,request,id):
        try:
            return self.model_class.objects.get(id=id)
        except self.model_class.DoesNotExist:
            return Response({'message':"No book found with this id"})

    def get(self, request, id):
        obj = self.get_obj(request, id=id)
        serializer = self.serializer_class(obj)
        return Response({
            'status': True,
            'book_details': serializer.data
        })

    def put(self, request, id):
        try:
            obj = self.get_obj(request, id=id)
            serializer = self.serializer_class(instance=obj,
                                               data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True,
                                 'message': "book details updated successfully",
                                 'data': serializer.data})
        except self.model_class.DoesNotExist:
            return Response({'message':"No book found with this id"})


    def delete(self,request,id):
        try:
            obj = self.get_obj(request, id=id)
            obj.delete()
            return Response({'message':"No book found with this id"})
        except self.model_class.DoesNotExist:
            return Response({'message':"No book found with this id"})
