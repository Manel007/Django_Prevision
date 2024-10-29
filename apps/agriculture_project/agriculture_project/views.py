from django.shortcuts import render, get_object_or_404, redirect
from .models import CropYield
from .forms import YieldForm


















import pandas as pd  # Add this import for pandas
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split




# List all yields
def yield_list(request):
    yields = CropYield.objects.all()
    return render(request, 'agriculture/yield_list.html', {'yields': yields})

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
    # Load and preprocess the data
    yield_data = pd.read_csv('C:/Users/ASUS/Desktop/django/Django_Prevision/yield_df.csv')
    yield_data.dropna(inplace=True)

    # Prepare data for the model
    X = yield_data[['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = yield_data['hg/ha_yield']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Define a threshold for "good" yield (you can adjust this value)
    threshold = 500  # Example threshold value

    # Create qualitative assessments
    assessments = ["Bon rendement" if pred >= threshold else "Mauvais rendement" for pred in y_pred]

    # Pair predictions with assessments
    predictions_with_assessments = list(zip(y_pred.tolist(), assessments))

    # Calculate percentages
    train_percentage = len(X_train) / len(X) * 100
    test_percentage = len(X_test) / len(X) * 100

    # Log percentages in the terminal
    print(f'Pourcentage d\'entraînement : {train_percentage:.2f}%')
    print(f'Pourcentage de test : {test_percentage:.2f}%')

    context = {
        'train_percentage': train_percentage,
        'test_percentage': test_percentage,
        'predictions_with_assessments': predictions_with_assessments  # Include paired data
    }

    return render(request, 'agriculture/yield_prediction.html', context)
