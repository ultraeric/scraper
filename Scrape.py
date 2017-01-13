import scraper

queue = scraper.Session.action_queue

get_action = scraper.Scraper.Get_Action()

scraper = scraper.Scraper.Scraper(site = 'https://www.google.com/finance', actions = [get_action])
scraper.populate_queue()

queue.run()
