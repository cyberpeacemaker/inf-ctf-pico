
# Bootmarklet
A bookmarklet is a bookmark that runs JavaScript instead of loading a webpage

# Bookmarktlet / Console / Snippets

### 1. The Console (The Scratchpad)
The Console is for **one-off commands** and immediate feedback. You use it when you're actively debugging or testing a single line of code.

* **Best for:** Checking a variable value, testing a quick `document.querySelector`, or seeing error logs.
* **Downside:** Once you refresh the page or move to a new tab, your code is gone. You have to re-type or "arrow-up" to find it again.

### 2. Snippets (The Developer’s Library)
Found inside the **Sources** tab of DevTools, Snippets allow you to write and save multi-line scripts that stay in your browser forever.

* **Best for:** Complex scripts you run often (e.g., a script that audits a page's SEO or a custom data scraper).
* **Workflow:** Open DevTools → Sources → Snippets → New Snippet → Run.
* **Advantage:** You get a full code editor with syntax highlighting and the ability to save your work without polluting your bookmarks.

### 3. Bookmarklets (The "One-Click" Shortcut)
Bookmarklets are built for **speed and accessibility.** They live on your browser's UI (the bookmarks bar), meaning you don't even have to open DevTools to use them.

* **Best for:** Actions you want to trigger instantly while browsing, or for users who aren't "technical" enough to open DevTools.
* **Workflow:** Click a button in your bookmarks bar. Done.
* **Advantage:** It works across different pages instantly without navigating through the DevTools interface.

---

### Comparison Table

| Feature | Console | Snippets | Bookmarklet |
| :--- | :--- | :--- | :--- |
| **Location** | DevTools (Bottom/Side) | DevTools (Sources tab) | Browser Bookmarks Bar |
| **Ease of Access** | Moderate (Must open DevTools) | High (Must open DevTools) | **Instant** (One click) |
| **Code Length** | Usually short | Long / Multi-line | Short (Must fit in a URL) |
| **Persistence** | Disappears on refresh | **Saved in Browser** | **Saved in Bookmarks** |
| **UI Interaction** | None | None | Can be clicked like a button |

