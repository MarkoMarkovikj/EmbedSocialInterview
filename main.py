import json
import tkinter as tk

WINHEIGHT = 900
WINWIDTH = 700
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


def filter_reviews(order_by_rating, min_rating, order_by_date, prioritize_by_text, window):
    reviews = load_reviews()

    filter_by_text(reviews, prioritize_by_text)
    filter_by_rating(reviews, order_by_rating)
    filter_by_date(reviews, order_by_date)
    filtered_reviews = filter_by_min_rating(reviews, int(min_rating))

    print(filtered_reviews)


def create_window():
    window = tk.Tk()
    window.title('Review filtering')

    canvas = tk.Canvas(window, height=WINHEIGHT, width=WINWIDTH)
    canvas.pack()

    frame = tk.Frame(window)
    frame.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.7)

    # ----------------------------------------------------------------------------------
    # Title
    title_label = tk.Label(frame, text='Filter reviews', font=FONT_LG)
    title_label.place(relx=0.05, rely=0.05, relwidth=0.3, relheight=0.1)

    # ----------------------------------------------------------------------------------
    # Order by rating
    order_by_rating_options = ['Highest First', 'Lowest First']

    order_by_rating_label = tk.Label(frame, text='Order by rating', font=FONT_SM)
    order_by_rating_label.place(relx=0.05, rely=0.15, relwidth=0.2, relheight=0.08)

    order_by_rating_var = tk.StringVar()
    order_by_rating_var.set(order_by_rating_options[0])

    order_by_rating_dropdown = tk.OptionMenu(frame, order_by_rating_var, *order_by_rating_options)
    order_by_rating_dropdown.place(relx=0.05, rely=0.23, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Minimum rating
    minimum_rating_options = ['1', '2', '3', '4', '5']

    minimum_rating_label = tk.Label(frame, text='Minimum Rating', font=FONT_SM)
    minimum_rating_label.place(relx=0.05, rely=0.35, relwidth=0.2, relheight=0.08)

    minimum_rating_var = tk.StringVar()
    minimum_rating_var.set(minimum_rating_options[0])

    minimum_rating_dropdown = tk.OptionMenu(frame, minimum_rating_var, *minimum_rating_options)
    minimum_rating_dropdown.place(relx=0.05, rely=0.43, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Order by date
    order_by_date_options = ['Oldest First', 'Newest First']

    order_by_date_label = tk.Label(frame, text='Order by date', font=FONT_SM)
    order_by_date_label.place(relx=0.05, rely=0.55, relwidth=0.2, relheight=0.08)

    order_by_date_var = tk.StringVar()
    order_by_date_var.set(order_by_date_options[0])

    order_by_date_dropdown = tk.OptionMenu(frame, order_by_date_var, *order_by_date_options)
    order_by_date_dropdown.place(relx=0.05, rely=0.63, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Prioritize by text
    prioritize_by_text_options = ['Yes', 'No']

    prioritize_by_text_label = tk.Label(frame, text='Prioritize by text', font=FONT_SM)
    prioritize_by_text_label.place(relx=0.05, rely=0.75, relwidth=0.2, relheight=0.08)

    prioritize_by_text_var = tk.StringVar()
    prioritize_by_text_var.set(prioritize_by_text_options[0])

    prioritize_by_text_dropdown = tk.OptionMenu(frame, prioritize_by_text_var, *prioritize_by_text_options)
    prioritize_by_text_dropdown.place(relx=0.05, rely=0.83, relwidth=0.9, relheight=0.08)

    # ----------------------------------------------------------------------------------
    # Filter button
    filter_button = tk.Button(frame, text='Filter', font=FONT_SM, bg='blue', fg='white',
                              command=lambda: filter_reviews(
                                  order_by_rating_var.get(),
                                  minimum_rating_var.get(),
                                  order_by_date_var.get(),
                                  prioritize_by_text_var.get(),
                                  window)
                              )

    filter_button.place(relx=0.05, rely=0.93, relwidth=0.15, relheight=0.05)

    return window


def main():
    window = create_window()
    window.mainloop()


if __name__ == '__main__':
    main()
