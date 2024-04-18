from django.shortcuts import render, redirect
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from faker import Faker
from application.models import Product, Category
import faker_commerce
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
   

class ProductSearializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class HomeView(APIView):
    # permission_classes = (IsAuthenticated,)
    faker = Faker()
    def get(self, request):
        product = Product.objects.all()
        product_data = ProductSearializer(product, many=True)

        return render(request, 'home.html', context={'data': product_data.data})
    
    def post(self, request):
        try:
            rows = request.data.get('product_row')
            print("rows", type(rows))
            for _ in range(int(rows)):
                print("rows", _)
                category = Category.objects.get(id=int(self.faker.random_number(1)))
                Product.objects.create(
                    category_id = category,
                    title = faker_commerce.PRODUCT_DATA['product'][self.faker.random_number(1)],
                    description = self.faker.text(),
                    price = int(self.faker.random_number(5)),
                    status = int(self.faker.pybool())
                ).save()
            return redirect('/')
        except Exception as e:
            print("Error : ", e)
            return Response("Error Found : ", status=status.HTTP_400_BAD_REQUEST)
        
class ProductView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = Product.objects.get(id=pk)
            product_data = ProductSearializer(product)
        else:
            product = Product.objects.all()
            product_data = ProductSearializer(product, many=True)
        return Response(product_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        category_id = request.data.get('category_id')
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        status = request.data.get('status')

        category = Category.objects.get(id=category_id)
        product = Product.objects.create(
                    category_id = category,
                    title = title,
                    description = description,
                    price = price,
                    status = status
                )
        product.save()
        return Response({"Message": "Product created successfully."})
    
    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSearializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Product updated successfully."}, status=status.HTTP_200_OK)
            # return Response({"Message": "Product updated successfully."}, status=status.HTTP_200_OK)
            return Response({"Message": "Error Found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Message": "Error Found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            if pk:
                product = Product.objects.get(id=pk)
                product.delete()
                return Response({"Message": "Product deleted successfully."}, status=status.HTTP_200_OK)
            return Response({"Message": "Error Found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Message": "Error Found"}, status=status.HTTP_400_BAD_REQUEST)