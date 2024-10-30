from django.shortcuts import render, get_object_or_404, redirect
from .models import CropYield
from .forms import YieldForm
from django.contrib.auth.decorators import login_required

import pandas as pd 
from django.http import HttpResponse
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from django.core.paginator import Paginator
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential 
from keras.layers import Dense
from django.shortcuts import render
from .forms import YieldPredictionForm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.shortcuts import render
from io import BytesIO
import base64
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from django.shortcuts import render, get_object_or_404, redirect
from .models import CropYield, Review
from .forms import YieldForm, ReviewForm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from io import BytesIO
import base64

from django.db.models import Q  
from django.shortcuts import render
@login_required(login_url="/login/")


def yield_list(request):
    query = request.GET.get('search', '')
    yields = CropYield.objects.all()

    if query:
        yields = yields.filter(
            Q(area__icontains=query) | Q(item__icontains=query) | Q(year__icontains=query)
        )

    paginator = Paginator(yields, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   
    return render(request, 'agriculture/yield_list.html', {'page_obj': page_obj, 'search_query': query})
@login_required(login_url="/login/")

def yield_detail(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  
    return render(request, 'agriculture/yield_detail.html', {'yield': yield_item})
@login_required(login_url="/login/")

def yield_create(request):
    if request.method == "POST":
        form = YieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm()
    return render(request, 'agriculture/yield_form.html', {'form': form})

@login_required(login_url="/login/")
def yield_update(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk) 
    if request.method == "POST":
        form = YieldForm(request.POST, instance=yield_item)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm(instance=yield_item)
    return render(request, 'agriculture/yield_form.html', {'form': form})

@login_required(login_url="/login/")
def yield_delete(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk) 
    if request.method == "POST":
        yield_item.delete()
        return redirect('yield_list')
    return render(request, 'agriculture/yield_confirm_delete.html', {'yield': yield_item})







   
  


@login_required(login_url="/login/")

def yield_prediction_view(request):
    form = YieldPredictionForm()
    prediction = None

    if request.method == 'POST':
        form = YieldPredictionForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            average_rain_fall = form.cleaned_data['average_rain_fall']
            pesticides = form.cleaned_data['pesticides']
            avg_temp = form.cleaned_data['avg_temp']


            yield_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv')

            yield_data.dropna(inplace=True)

            X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
            y = yield_data['hg/ha_yield']

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

            model = LinearRegression()

            model.fit(X_train, y_train)

            new_data = scaler.transform([[year, average_rain_fall, pesticides, avg_temp]])
            prediction = model.predict(new_data)

    context = {
        'form': form,
        'prediction': prediction.flatten() if prediction is not None else None
    }
    return render(request, 'front/yield_prediction.html', context)



@login_required(login_url="/login/")



def review_list(request, yield_id):
    crop_yield = get_object_or_404(CropYield, pk=yield_id)
    reviews = crop_yield.reviews.all()
    return render(request, 'front/review_list.html', {'crop_yield': crop_yield, 'reviews': reviews})
@login_required(login_url="/login/")

def create_review(request, yield_id):
    crop_yield = get_object_or_404(CropYield, pk=yield_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False) 
            review.crop_yield = crop_yield  
            review.save()  
            return redirect('review_list', yield_id=crop_yield.id)
    else:
        form = ReviewForm()  

    return render(request, 'front/review_form.html', {'form': form, 'crop_yield': crop_yield})
@login_required(login_url="/login/")


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    crop_yield = review.crop_yield 

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)  
        if form.is_valid():
            form.save()  
            return redirect('review_list', yield_id=crop_yield.id)
    else:
        form = ReviewForm(instance=review)  

    return render(request, 'front/review_form.html', {'form': form, 'crop_yield': crop_yield})
@login_required(login_url="/login/")

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    yield_id = review.crop_yield.id
    if request.method == "POST":
        review.delete()
        return redirect('review_list', yield_id=yield_id)
    return render(request, 'front/review_confirm_delete.html', {'review': review})
@login_required(login_url="/login/")

def yield_summary(request):
    query = request.GET.get('search', '')
    yields = CropYield.objects.all()

    if query:

        yields = yields.filter(
            Q(item__icontains=query) | Q(year__year=query) 
        )

    paginator = Paginator(yields, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'front/yield_summary.html', {'page_obj': page_obj, 'search_query': query})















def yield_classification_view(request):

    yield_data = pd.read_csv('C:/Users/user/Desktop/black-dashboard-django-master/black-dashboard-django-master/yield_df.csv')


    high_threshold = 60000
    medium_threshold = 30000
    yield_data['yield_class'] = yield_data['hg/ha_yield'].apply(lambda x: 'High' if x >= high_threshold else ('Medium' if x >= medium_threshold else 'Low'))

    X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = yield_data['yield_class']  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    test_results = X_test.copy()
    test_results['Predicted Class'] = y_pred
    test_results['Actual Class'] = y_test

    plt.figure(figsize=(12, 6))
    sns.countplot(data=test_results, x='Year', hue='Predicted Class')
    plt.title("Crop Yield Classification by Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend(title='Yield Class')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    context = {
        'graphic': graphic
    }
    return render(request, 'agriculture/yieldd_classification.html', context)




