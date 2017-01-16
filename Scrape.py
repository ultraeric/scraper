import scraper

queue = scraper.Session.action_queue

get_action = scraper.Scraper.Get_Action()

scrapers = []
for i in range(100):
	scraper1 = scraper.Scraper.Scraper(site = 'https://www.google.com/finance', actions = [get_action])
	scrapers.append(scraper1)

queue.populate_queue()
queue.run()
