# WordPress blog content extraction

This project started as a personal effort to help a client preserve the content on her WordPress website. She had been writing valuable blog posts for years, but entries from 2012 to 2023 had accumulated inside one very large WordPress post. The outdated theme also made the site difficult to modernise and use on mobile devices.

I wanted to make the content easier to preserve, search, and eventually present on a new website. I wrote a Python scraper to split the large WordPress post into individual entries and convert them into Markdown files.

## What the scraper did

The scraper:

- fetched the original WordPress page;
- split the large post into individual entries;
- extracted titles, dates, categories, text, and image links; and
- wrote the entries as Markdown files with front matter for Hugo.

The original HTML was inconsistent, so this was not a fully automated migration. The extracted files needed manual corrections and cleanup as well. The main result is the collection of individual Markdown posts in [`content/blog`](content/blog), covering 2012 to June 2023.

The scraper is in [`content/scraper/scraper.py`](content/scraper/scraper.py). Its current entry point can be run with:

```bash
python content/scraper/scraper.py
```

It downloads the WordPress page and may download referenced images while generating files, so it should be treated as an extraction script rather than a repeatable build step. The script's dependencies include `requests`, `beautifulsoup4`, and `html2text`.

## Hugo experiment and current status

I later experimented with Hugo and the `hugo-theme-walden` theme. I initially hoped to move the client toward editing the site through a workflow using an editor and GitHub, but that turned out to be too optimistic for this project. I did not finish the Hugo setup, and the rebuilt website was never put live.

The content extraction and preparation are the finished parts of this project. The Hugo configuration and theme submodule remain as a record of the unfinished presentation experiment.
