import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql://root:chiquet@localhost/sakila')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Sakila Queries"),

    dcc.Dropdown(
        id='query-dropdown',
        options=[
            {'label': 'Rental Data Over Time', 'value': 1},
            {'label': 'Movies per Actor', 'value': 2},
            {'label': 'Revenue per Film', 'value': 3},
            {'label': 'Payments per Customer', 'value': 4},
            {'label': 'Movies per Rating', 'value': 5},
        ],
        value=1  # Default selected option
    ),
    
    html.Div(id='query-display'),

    html.H1("Rental Data Over Time"),
    dcc.Graph(id='query-1-graph'),
    
    html.H1("Movies per Actor"),
    dcc.Graph(id='query-2-graph'),
    
    html.H1("Revenue per Film"),
    dcc.Graph(id='query-3-graph'),
    
    html.H1("Payments per Customer"),
    dcc.Graph(id='query-4-graph'),
    
    html.H1("Movies per Rating"),
    dcc.Graph(id='query-5-graph'),
])


# Query 1
@app.callback(
    Output('query-1-graph', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_line_chart(selected_query):
    # SQL query to retrieve data for the selected category over time
    query1 = f"""
    SELECT DATE(rental_date) AS rental_day, COUNT(rental_id) AS rental_count
    FROM rental, inventory, film, film_category
    WHERE rental.inventory_id = inventory.inventory_id AND
    inventory.film_id = film.film_id AND
    film.film_id = film_category.film_id AND
    category_id = 1
    GROUP BY rental_day;
    """

    rental_data = pd.read_sql(query1, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['rental_day'],
                'y': rental_data['rental_count'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count',
            'xaxis': {'title': 'Rental Day'},
            'yaxis': {'title': 'Rental Count'}
        }
    }

    return fig




@app.callback(
    Output('query-2-graph', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_graphs(selected_query):
    query2 = f"""
    SELECT actor.actor_id, CONCAT(actor.first_name, ' ', actor.last_name) AS actor_name, COUNT(film_actor.actor_id) AS movie_count
    FROM actor
    JOIN film_actor ON actor.actor_id = film_actor.actor_id
    GROUP BY actor.actor_id
    HAVING movie_count >= 20
    ORDER BY movie_count DESC;
    """


    rental_data = pd.read_sql(query2, engine)

    fig = {
        'data': [
            {
                'x': rental_data['actor_name'],
                'y': rental_data['movie_count'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Movie Count',
            'xaxis': {'title': 'Actor Name'},
            'yaxis': {'title': 'Movie Count'}
        }
    }

    return fig




@app.callback(
    Output('query-3-graph', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_graphs(selected_query):
    query3 = f"""
    SELECT film.title AS film_name, SUM(payment.amount) AS total_earnings
    FROM payment
    JOIN rental ON payment.rental_id = rental.rental_id
    JOIN inventory ON rental.inventory_id = inventory.inventory_id
    JOIN film ON inventory.film_id = film.film_id
    GROUP BY film.title
    ORDER BY total_earnings DESC;
    """

    rental_data = pd.read_sql(query3, engine)

    fig = {
        'data': [
            {
                'x': rental_data['film_name'],
                'y': rental_data['total_earnings'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Revenue Count',
            'xaxis': {'title': 'Film Name'},
            'yaxis': {'title': 'Film Revenue'}
        }
    }

    return fig




@app.callback(
    Output('query-4-graph', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_graphs(selected_query):
    query4 = f"""
    SELECT c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, SUM(p.amount) AS total_payments
    FROM customer AS c
    JOIN payment AS p ON c.customer_id = p.customer_id
    GROUP BY c.customer_id, customer_name
    ORDER BY total_payments DESC;
    """


    rental_data = pd.read_sql(query4, engine)

    fig = {
        'data': [
            {
                'x': rental_data['customer_name'],
                'y': rental_data['total_payments'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Payments',
            'xaxis': {'title': 'Customer Name'},
            'yaxis': {'title': 'Total Customer Payments'}
        }
    }

    return fig




@app.callback(
    Output('query-5-graph', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_graphs(selected_query):
    query5 = f"""
    SELECT rating, COUNT(*) AS rating_count
    FROM film
    GROUP BY rating
    ORDER BY rating_count DESC;
    """


    rental_data = pd.read_sql(query5, engine)

    fig = {
        'data': [
            {
                'x': rental_data['rating'],
                'y': rental_data['rating_count'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Movies per Rating',
            'xaxis': {'title': 'Rating'},
            'yaxis': {'title': 'Rating Count'}
        }
    }

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
