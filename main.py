from bookingmodule.booking import Booking
import time


def main():
    with Booking() as bot:
        bot.get_landing_page()
        # bot.change_currency
        time.sleep(1)
        bot.reject_cookies()
        bot.search("chennai")
        bot.trip_dates("2022-08-03", "2022-08-07")
        bot.no_people(2)
        bot.search_btn()
        bot.get_report()
        time.sleep(120)

if __name__ == '__main__':
    main()
