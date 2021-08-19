import json
import tkinter as tk
from tkinter import ttk

WINHEIGHT = 900
WINWIDTH = 750
FONT_LG = 'Helvetica 16 bold'
FONT_SM = 'Helvetica 10'


def load_reviews():
    with open('reviews.json') as file:
        reviews = json.load(file)

    return reviews


def filter_by_text(reviews, prioritize_by_text):
    if prioritize_by_text == 'Yes':
        reviews.sort(key=lambda review: review['reviewText'] != '', reverse=True)


def filter_by_rating(reviews, order_by_rating):
    reverse = order_by_rating == 'Highest First'

    reviews.sort(key=lambda review: review['rating'], reverse=reverse)


def filter_by_date(reviews, order_by_date):
    reverse = order_by_date == 'Newest First'

    reviews.sort(key=lambda review: review['reviewCreatedOnTime'], reverse=reverse)


def filter_by_min_rating(reviews, min_rating):
    return list(filter(lambda r: r['rating'] >= min_rating, reviews))


def save_as_json(filtered_reviews):
    with open('filtered_reviews.json', 'w') as file:
        json.dump(filtered_reviews, file)


def filter_reviews(order_by_rating, min_rating, order_by_date, prioritize_by_text, window):
    reviews = load_reviews()

    filtered_reviews = filter_by_min_rating(reviews, int(min_rating))
    filter_by_date(filtered_reviews, order_by_date)
    filter_by_rating(filtered_reviews, order_by_rating)
    filter_by_text(filtered_reviews, prioritize_by_text)
    
    save_as_json(filtered_reviews)
    run(filtered_reviews, window)


def get_content_from_review(review):
    return f'Rating: {"".join(["*" for _ in range(review["rating"])])}' + '\n' \
           f'Text: {review["reviewText"]}' + '\n' \
           f'Likes: {review["numLikes"]}' + '\n' \
           f'Created on: {review["reviewCreatedOnDate"]}'


def get_window(reviews: list = None, window: tk.Tk = None):
    if reviews is None:
        reviews = []
    # Create a new window if its not passed
    if window is None:
        window = tk.Tk()

    window.title('Review filtering')
    window.geometry(f'{WINWIDTH}x{WINHEIGHT}')

    form_frame = tk.Frame(window)
    form_frame.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.6)

    # ----------------------------------------------------------------------------------
    # Title
    title_label = tk.Label(form_frame, text='Filter reviews', font=FONT_LG)
    title_label.place(relx=0.05, rely=0.05, relwidth=0.3, relheight=0.1)

    # ----------------------------------------------------------------------------------
    # Order by rating
    order_by_rating_options = ['Highest First', 'Lowest First']

    order_by_rating_label = tk.Label(form_frame, text='Order by rating', font=FONT_SM)
    order_by_rating_label.place(relx=0.05, rely=0.15, relwidth=0.2, relheight=0.08)

    order_by_rating_var = tk.StringVar()
    order_by_rating_var.set(order_by_rating_options[0])

    order_by_rating_dropdown = tk.OptionMenu(form_frame, order_by_rating_var, *order_by_rating_options)
    order_by_rating_dropdown.place(relx=0.05, rely=0.23, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Minimum rating
    minimum_rating_options = ['1', '2', '3', '4', '5']

    minimum_rating_label = tk.Label(form_frame, text='Minimum Rating', font=FONT_SM)
    minimum_rating_label.place(relx=0.05, rely=0.35, relwidth=0.2, relheight=0.08)

    minimum_rating_var = tk.StringVar()
    minimum_rating_var.set(minimum_rating_options[0])

    minimum_rating_dropdown = tk.OptionMenu(form_frame, minimum_rating_var, *minimum_rating_options)
    minimum_rating_dropdown.place(relx=0.05, rely=0.43, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Order by date
    order_by_date_options = ['Oldest First', 'Newest First']

    order_by_date_label = tk.Label(form_frame, text='Order by date', font=FONT_SM)
    order_by_date_label.place(relx=0.05, rely=0.55, relwidth=0.2, relheight=0.08)

    order_by_date_var = tk.StringVar()
    order_by_date_var.set(order_by_date_options[0])

    order_by_date_dropdown = tk.OptionMenu(form_frame, order_by_date_var, *order_by_date_options)
    order_by_date_dropdown.place(relx=0.05, rely=0.63, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Prioritize by text
    prioritize_by_text_options = ['Yes', 'No']

    prioritize_by_text_label = tk.Label(form_frame, text='Prioritize by text', font=FONT_SM)
    prioritize_by_text_label.place(relx=0.05, rely=0.75, relwidth=0.2, relheight=0.08)

    prioritize_by_text_var = tk.StringVar()
    prioritize_by_text_var.set(prioritize_by_text_options[0])

    prioritize_by_text_dropdown = tk.OptionMenu(form_frame, prioritize_by_text_var, *prioritize_by_text_options)
    prioritize_by_text_dropdown.place(relx=0.05, rely=0.83, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Filter button
    filter_button = tk.Button(form_frame, text='Filter', font=FONT_SM, bg='blue', fg='white',
                              command=lambda: filter_reviews(
                                  order_by_rating_var.get(),
                                  minimum_rating_var.get(),
                                  order_by_date_var.get(),
                                  prioritize_by_text_var.get(),
                                  window)
                              )

    filter_button.place(relx=0.05, rely=0.93, relwidth=0.15, relheight=0.05)

    # ----------------------------------------------------------------------------------
    # Reviews frame

    if reviews:  # If reviews is not empty create the frame
        reviews_frame = tk.Frame(window, borderwidth=2, relief="groove")
        reviews_frame.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.3)

        reviews_canvas = tk.Canvas(reviews_frame)
        scrollbar = ttk.Scrollbar(reviews_frame, orient="vertical", command=reviews_canvas.yview)
        scrollable_frame = ttk.Frame(reviews_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: reviews_canvas.configure(
                scrollregion=reviews_canvas.bbox("all")
            )
        )

        reviews_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        reviews_canvas.configure(yscrollcommand=scrollbar.set)

        for review in reviews:  # add all the filtered reviews to the frame
            review_content = get_content_from_review(review)
            review_label = tk.Label(scrollable_frame, text=review_content)
            review_label.pack(pady=5, side=tk.TOP, anchor="w")

        reviews_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    return window


def run(reviews=None, window=None):
    window = get_window(reviews, window)
    window.mainloop()


def main():
    run()


if __name__ == '__main__':
    main()
