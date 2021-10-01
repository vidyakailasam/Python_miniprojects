from selenium import webdriver
from bs4 import BeautifulSoup
import time
import tkinter as tk
import re
import requests
import pandas as pd
import random
from tkinter import ttk



def popup(msg):
    popup = tk.Tk()
    popup.wm_title("Flights Data ")
    NORM_FONT = ("Verdana", 20)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def search_hotel():
    try:
        location = e1.get()
        check_in_date = e2.get()
        check_out_date = e3.get()
        no_of_rooms = e4.get()
        guests = e5.get()
        # location = 'chennai'
        # check_in_date = '20210920'
        # check_out_date = '20210921'
        # no_of_rooms = '1'
        # guests = '2'

        url = "https://www.goibibo.com/hotels/find-hotels-in-" + location + "/4354390963378411938/4354390963378411938/%7B%22ci%22:%22" + check_in_date + "%22,%22co%22:%22" + check_out_date + "%22,%22r%22:%22" + no_of_rooms + "-" + guests + "-0%22%7D/?{%22filter%22:{}}&sec=dom&cc=IN"

        # .format(location, check_in_date, check_out_date, no_of_rooms, guests)
        r = requests.get(url)
        # print(r.text)
        print(f"URL: {url}")
        print("The cheapest Hotels: \n")

        driver = webdriver.Firefox(executable_path='/home/vidya/Desktop/geckodriver')
        driver.get(url)
        time.sleep(10)

        droupdown = driver.find_element_by_xpath('//span[contains(@class,"Sortingstyles__WrapperSpan-sc")]')

        if droupdown:
            droupdown.click()
            time.sleep(5)
            priceLowtoHigh = driver.find_elements_by_xpath('//span[contains(text(),"Price (Low to High)")]')
            if priceLowtoHigh:
                priceLowtoHigh[0].click()
                time.sleep(10)
                # randomClick = driver.find_elements_by_xpath('//span')
                # if randomClick:
                #     randomClick[0].click()
                #     time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # hotel_names = driver.find_element_by_xpath('//h4[contains(@class,"dwebCommonstyles__SmallSectionHeader-sc-112ty3f-7")]')

        # time.sleep(10)
        driver.quit()
        # hotel_names = soup.findAll('div', attrs={'class':'HotelCardstyles__HotelNameWrapperDiv-sc-1s80tyk-12 biniNQ'})

        hotel_names = soup.find_all('h4', attrs={'class': re.compile('dwebCommonstyles__SmallSectionHeader-sc')})
        hotel_prices = soup.find_all('p', attrs={'class': re.compile('HotelCardstyles__CurrentPrice-sc-')})
        hotel_ratings = soup.find_all('span',
                                      attrs={'class': re.compile('ReviewAndRatingsstyles__AverageReviewText-sc')})
        nearest_locations = soup.find_all('div', attrs={
            'class': re.compile('PersuasionHoverTextstyles__TextWrapperSpan-sc-1c06rw1-14 cTsPPE')})
        # hotel_names = soup.find_all('//h4[contains("class","dwebCommonstyles__SmallSectionHeader-sc-112ty3f-7")]')
        # Getting all the data from the website using html elements and tags.
        hotel_names_list = [a.getText().strip() for a in hotel_names]
        hotel_prices_list = [a.getText().strip() for a in hotel_prices]
        hotel_ratings_list = [a.getText().strip() for a in hotel_ratings]
        nearest_locations_list = [a.getText().strip() for a in nearest_locations]

        new_nearest_locations_list = []
        for i in range(len(nearest_locations_list)):
            if i % 2 == 0:
                str1 = nearest_locations_list[i]
                str2 = nearest_locations_list[i + 1]
                new_nearest_locations_list.append(str1 + ", " + str2)

        hotel_details = {
            "Hotel Name": hotel_names_list,
            "Hotel Price": hotel_prices_list,
            "Rating": hotel_ratings_list,
            "Nearest": new_nearest_locations_list
        }

        hotel_info = pd.DataFrame(hotel_details)

        print(hotel_info)
        file_name = "hotel_info-" + str(random.randint(0, 100)) + ".xlsx"
        hotel_info.to_excel(file_name, index=None)

        popup("Hotel Date Fetched Successfully !!..")
    except Exception as e:
        print(e.with_traceback())
        popup("Error while Fetching the Data Please try again after some time.....")

root = tk.Tk()
text = tk.Text(root, bg='light blue')
text.grid(row=6, column=0, columnspan=2)
root.title('Mini Project Find Chepest Hotels')

tk.Label(root, text="Enter City : ").grid(row=0)
e1 = tk.Entry(root)
e1.grid(row=0, column=1)

tk.Label(root, text="Enter Check-In date (YYYYmmdd): ").grid(row=1)
e2 = tk.Entry(root)
e2.grid(row=1, column=1)

tk.Label(root, text="Enter Check-out Date (YYYYmmdd): ").grid(row=2)
e3 = tk.Entry(root)
e3.grid(row=2, column=1)

tk.Label(root, text="Enter No Of Rooms : ").grid(row=3)
e4 = tk.Entry(root)
e4.grid(row=3, column=1)

tk.Label(root, text="Enter No Of Guests : ").grid(row=4)
e5 = tk.Entry(root)
e5.grid(row=4, column=1)

tk.Button(root,
              text='Search', command=search_hotel, anchor=tk.CENTER).grid(row=5, column=1,
                                                                          sticky=tk.W,
                                                                          pady=4)
root.mainloop()




