/* Extract meaningful content from the downloaded html in the out/ directory.
   Output to clean.html for each html file.
*/
const Apify = require('apify');
const fse = require('fs-extra');
//const dbUtils = require('./util/db_utils.js');
const gotoExtended = Apify.utils.puppeteer.gotoExtended;
const moment = require('moment');
const globby = require('globby');
const Mercury = require('@postlight/mercury-parser');
//const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const strings = require('@util.js/strings')


const outputDir = './out';
(async () => {
  const requestList = new Apify.RequestList({
    sources: process.argv.slice(2),
    //persistStateKey: 'privacy-policy-state',
    //persistSourcesKey: 'privacy-policy-sources'
  });
  await requestList.initialize();

  const crawler = new Apify.PuppeteerCrawler({
      requestList,
      maxRequestsPerCrawl: 10,
      gotoFunction: async ({ page, request }) => {
          let timeoutMs = 60000;
          return gotoExtended(page, request, { timeout: timeoutMs, waitUtil: 'networkidle2'});
      },
      handlePageFunction: async ({request, page}) => {

          /* Create directory to store the files */
          const title = await page.title();
          let appId = request.url;
          let finalDest = `${outputDir}/${title}`;
          fse.ensureDirSync(finalDest);

          /* Print page title */
          console.log(`*** Processing ${request.url}: ${title}, ${appId}`);
          console.log(finalDest)

          /* Scrape MHTML */
          const cdp = await page.target().createCDPSession();
          const {data} = await cdp.send('Page.captureSnapshot', {format: 'mhtml'});
          fse.writeFileSync(`${finalDest}/page.mhtml`, data);

          /* Scrape HTML */
          const renderedContent = await page.evaluate(() => new XMLSerializer().serializeToString(document));
          fse.writeFileSync(`${finalDest}/page.html`, renderedContent);
          /* Write metadata */
          let metadata = {
              url: request.url,
              accessedDate: moment().format()
          };
          fse.writeFileSync(`${finalDest}/metadata.json`, JSON.stringify(metadata));
        }
    });

    /* Finally, run the crawler */
    await crawler.run();

  const dirPaths = await globby(['out/*'], {onlyFiles: false});
  for (const dirPath of dirPaths) {
      console.log(`Processing ${dirPath}`);
      const pageHtmlPath = `${dirPath}/page.html`;
      const metadataPath = `${dirPath}/metadata.json`;

      Promise.all([fse.readFile(pageHtmlPath), fse.readFile(metadataPath)])
          .then(([pageHtml, metadataText]) => {
              metadata = JSON.parse(metadataText);
              Mercury.parse(metadata.url, { html: pageHtml, contentType: 'html' }).then(result => {
                  fse.writeFileSync(`${dirPath}/clean.html`, result.content);
              })
              .catch(console.error);
          })
          .catch(console.error);

      const cleanHTMLPath = `${dirPath}/clean.html`;
      console.log(`Processing ${cleanHTMLPath}`);
  }

}) ();
