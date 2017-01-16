# vis

<h1>Environment Setup</h1>
<ol>
  <li>Clone repository into directory of your choice and navigate to vis folder (hereto referenced as &lt;vis_home&gt;)</li>
  <li>Navigate to .../&lt;vis_home&gt;/ and run the command <code>sudo sh setup_env.sh</code>. 
  <li>Run the command in the CL <code>python3 setup.py install</code> 
</ol>
<h1>Usage</h1>
<p>To begin utilizing this module, first do <code>import scraper</code>. This imports <code>scraper.Session</code> which will keep track of the scraping session that you are currently running and handle multi-threading internally.</p>
<p>In the <b>Scraper</b> module there are two important classes: <b>Scraper</b> and <b>Action</b>. As a rule of thumb, <b>Scraper</b> is the information source, while <b>Action</b> is an action that acts on the information present in a Scraper.</p> 
<h2>Scraper</h2>
<p>This class is the source of truth for any Action that acts on the scraper. Note that this means the Scraper itself does not actually do anything; you submit actions to this Scraper, initialize the Actions, and then run the queue.</p>
<h2>Action</h2>
<p>This class's instances act on a Scraper. To run an action immediately, you can use <code>Action.execute(self)</code>. To spawn an action that attaches to the queue and runs when the resources are available, use <code>Action.run(self)</code>. Running the latter will attach an action method to the Session queue which will run when an available thread can handle it.</p>
<p>To create custom actions, extend the Action class and override the <code>Action.get_act(self, scraper)</code> method. This should return a higher-order function that will be run and act on the information stored in the Scraper. It is possible to chain together Actions by creating, in the higher-order function, sub-actions and using <code>Action.execute(scraper)</code> to immediately run the action, thereby stringing together functionality and consolidating it into a single Action.</p>
<h2>Examples</h2>

```
import scraper
queue = scraper.Session.action_queue
get_action = scraper.Scraper.Get_Action()
scraper1 = scraper.Scraper.Scraper(site = 'https://www.google.com/', actions = [get_action])
queue.populate_queue()
queue.run()
```
