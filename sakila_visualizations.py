from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'username' and 'password' with your MySQL username and password
engine = create_engine('mysql://root:chiquet@localhost/sakila')
query = """
    SELECT rating, COUNT(*) AS rating_count
    FROM film
    GROUP BY rating
    ORDER BY rating_count DESC;
    """

# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query, engine)


# Set the figure size
plt.figure(figsize=(10, 6))

# Create a bar chart
plt.bar(rental_data['rating'], rental_data['rating_count'])

# Customize the chart
plt.title('Number of Rentals by Category')
plt.xlabel('Category')
plt.ylabel('Rental Count')
plt.xticks(rotation=45)  # Rotate category labels for readability

# Display the chart
plt.tight_layout()
plt.show()