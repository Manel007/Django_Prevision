from django.shortcuts import render, get_object_or_404, redirect
from .models import CropYield
from .forms import YieldForm
import pandas as pd 
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

from django.db.models import Q  # Ajoutez cette ligne
from django.shortcuts import render

def yield_list(request):
    query = request.GET.get('search', '')
    yields = CropYield.objects.all()

    if query:
        # Utilisez Q pour combiner les filtres
        yields = yields.filter(
            Q(area__icontains=query) | Q(item__icontains=query) | Q(year__icontains=query)
        )

    paginator = Paginator(yields, 10)  # 10 rendements par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'agriculture/yield_list.html', {'page_obj': page_obj, 'search_query': query})
# Yield details
def yield_detail(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    return render(request, 'agriculture/yield_detail.html', {'yield': yield_item})

# Create new yield
def yield_create(request):
    if request.method == "POST":
        form = YieldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm()
    return render(request, 'agriculture/yield_form.html', {'form': form})

# Update a yield
def yield_update(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    if request.method == "POST":
        form = YieldForm(request.POST, instance=yield_item)
        if form.is_valid():
            form.save()
            return redirect('yield_list')
    else:
        form = YieldForm(instance=yield_item)
    return render(request, 'agriculture/yield_form.html', {'form': form})

# Delete a yield
def yield_delete(request, pk):
    yield_item = get_object_or_404(CropYield, pk=pk)  # Corrected model name
    if request.method == "POST":
        yield_item.delete()
        return redirect('yield_list')
    return render(request, 'agriculture/yield_confirm_delete.html', {'yield': yield_item})



#Regr Linéaire 
def yield_prediction_view(request):
   
    # Load and preprocess data
    yield_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/yield_df.csv')
    # Load and preprocess the data

    # Load and preprocess data
         #yield_data = pd.read_csv('C:/Users/oumai/Desktop/Django_Prevision/yield_df.csv')

    yield_data.dropna(inplace=True)
    
    # Prepare data for model training
    X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = yield_data['hg/ha_yield']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Graphical representation of actual vs predicted yields
    plt.figure(figsize=(10, 6))
    sns.regplot(x=y_test, y=y_pred, scatter_kws={'alpha':0.5})
    plt.xlabel("Valeurs réelles")
    plt.ylabel("Valeurs prédites")
    plt.title("Prédictions des rendements agricoles")
    
    # Save plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    context = {
        'graphic': graphic
    }
    return render(request, 'agriculture/yield_prediction.html', context)


def yield_classification_view(request):
    # Load the data
    yield_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/yield_df.csv')
        #yield_data = pd.read_csv('C:/Users/oumai/Desktop/Django_Prevision/yield_df.csv')

    # Define the threshold
    threshold = 500

    # Create a binary column for good or bad yield
    yield_data['rendement_class'] = yield_data['hg/ha_yield'].apply(lambda x: 1 if x >= threshold else 0)

    # Prepare features and target variable
    X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = yield_data['rendement_class']  # Binary classification

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest Classifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Classification report
    report = classification_report(y_test, y_pred)

    # Pass the report to the template
    context = {
        'report': report  # Pass the report to the template
    }
    return render(request, 'agriculture/yield_classification.html', context)


# Assurez-vous de charger votre modèle ici
# Par exemple: model = load_model('path_to_your_model.h5')from django.shortcuts import render


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

            # Charger les données pour entraîner le modèle

            yield_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/yield_df.csv')

                #yield_data = pd.read_csv('C:/Users/oumai/Desktop/Django_Prevision/yield_df.csv')
            yield_data.dropna(inplace=True)

            # Préparation des données
            X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
            y = yield_data['hg/ha_yield']

            # Standardisation des caractéristiques (facultatif)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Diviser les données
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

            # Initialiser le modèle de régression linéaire
            model = LinearRegression()

            # Entraîner le modèle
            model.fit(X_train, y_train)

            # Préparation des nouvelles données pour la prédiction
            new_data = scaler.transform([[year, average_rain_fall, pesticides, avg_temp]])
            prediction = model.predict(new_data)

    context = {
        'form': form,
        'prediction': prediction.flatten() if prediction is not None else None
    }
    return render(request, 'front/yield_prediction.html', context)






# Review List for Specific Crop Yield
def review_list(request, yield_id):
    crop_yield = get_object_or_404(CropYield, pk=yield_id)
    reviews = crop_yield.reviews.all()
    return render(request, 'front/review_list.html', {'crop_yield': crop_yield, 'reviews': reviews})

# Create Review
from django.shortcuts import get_object_or_404, redirect, render
from .models import CropYield, Review
from .forms import ReviewForm

def create_review(request, yield_id):
    crop_yield = get_object_or_404(CropYield, pk=yield_id)

    print("Request Method:", request.method)  # Debugging
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging
            review = form.save(commit=False)
            review.crop_yield = crop_yield
            review.save()
            return redirect('review_list', yield_id=crop_yield.id)
        else:
            print("Form Errors:", form.errors)  # Debugging
    else:
        form = ReviewForm()

    return render(request, 'front/review_form.html', {'form': form, 'crop_yield': crop_yield})
    # Get the CropYield object or return a 404 if it doesn't exist
    crop_yield = get_object_or_404(CropYield, pk=yield_id)
    
    if request.method == "POST":
        # Bind the form with POST data
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Create a Review instance but don't save to the database yet
            review = form.save(commit=False)
            review.crop_yield = crop_yield
            review.save()  # Now save to the database
            return redirect('review_list', yield_id=crop_yield.id)
    else:
        form = ReviewForm()  # Provide an empty form if the request is GET
    
    # Render the form template with the form and crop_yield context
    return render(request, 'front/review_form.html', {'form': form, 'crop_yield': crop_yield})

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    crop_yield = review.crop_yield  # Get associated crop yield

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            # Redirect to review list for the associated crop yield
            return redirect('review_list', yield_id=crop_yield.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'front/review_form.html', {'form': form, 'crop_yield': crop_yield})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    yield_id = review.crop_yield.id
    if request.method == "POST":
        review.delete()
        return redirect('review_list', yield_id=yield_id)
    return render(request, 'front/review_confirm_delete.html', {'review': review})
def yield_summary(request):
    query = request.GET.get('search', '')
    yields = CropYield.objects.all()

    if query:

        yields = yields.filter(
            Q(item__icontains=query) | Q(year__year=query)  # Filtering by item and year as year field can be a date
        )

    paginator = Paginator(yields, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'front/yield_summary.html', {'page_obj': page_obj, 'search_query': query})















def yield_classification_view(request):
    # Load the data

    yield_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/yield_df.csv')

        #yield_data = pd.read_csv('C:/Users/oumai/Desktop/Django_Prevision/yield_df.csv')

    # Define thresholds and create a class column
    high_threshold = 60000
    medium_threshold = 30000
    yield_data['yield_class'] = yield_data['hg/ha_yield'].apply(lambda x: 'High' if x >= high_threshold else ('Medium' if x >= medium_threshold else 'Low'))

    # Prepare features and target variable
    X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = yield_data['yield_class']  # Using the newly created class column

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest Classifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Create a DataFrame for visualization
    test_results = X_test.copy()
    test_results['Predicted Class'] = y_pred
    test_results['Actual Class'] = y_test

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.countplot(data=test_results, x='Year', hue='Predicted Class')
    plt.title("Crop Yield Classification by Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend(title='Yield Class')
    
    # Save plot to a bytes buffer
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



# apps/agriculture_project/agriculture_project/views.py
import pandas as pd
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

def crop_classification_view(request):
    # Load the crop data
    try:

        crop_data = pd.read_csv('C:/Users/rebhi/OneDrive/Bureau/Django_Prevision/yield_df.csv')
            #crop_data = pd.read_csv('C:/Users/oumai/Desktop/Django_Prevision/yield_df.csv')

        # Check the columns to ensure they're correct
        print(crop_data.columns)  # Debugging line to print column names
        
        # Use the correct columns for training the model
        X = crop_data[['avg_temp', 'average_rain_fall_mm_per_year']]  # Updated column names
        y = crop_data['Item']  # Assuming 'Item' is your target variable for classification
        
        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the k-NN classifier
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)

        # Make predictions
        y_pred = knn.predict(X_test)

        # Generate a classification report
        report = classification_report(y_test, y_pred)

        context = {
            'report': report
        }
        return render(request, 'agriculture/crop_classification.html', context)

    except FileNotFoundError:
        return HttpResponse("Dataset not found.")
    except KeyError as e:
        return HttpResponse(f"KeyError: {str(e)} - Check your column names.")
