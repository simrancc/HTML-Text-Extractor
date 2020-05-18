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
          //const title = await page.title();
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

      fse.readFile(cleanHTMLPath, 'utf8', dataLoaded);

      function dataLoaded(err, data) {
        $ = cheerio.load('' + data + '');
        //console.log($.html($('ul')[0]));
        $('p').each(function (i, elem) {
          const str = $(this).text();
          const colon = str.lastIndexOf(":")
          console.log(colon)
          if (colon == str.length - 2 && colon != -1) {
            if ($(this).next()[0].name == 'ul' || $(this).next()[0].name == 'li' || $(this).next()[0].name == 'ol') {
              const children = $(this).next()[0].children
              var newPar = "";
              var combine = "";
              var check = false;
              var count = 0;
              for (const child of children) {
                if (child.type == 'tag') {
                  count = count + 1;
                  for (const x of child.children) {
                    if (x.type == 'text') {
                      text = x.data
                      if (count == 1 && text.length < 20) {
                        combine = combine + text + ", ";
                        check = true;
                      }
                      if (!check) {
                        newPar = str + text;
                        console.log(newPar);
                        console.log();
                      }
                      else if (check && count != 1) {
                        combine = combine + text + ", ";
                      }
                    }
                  }
                }
              }
              if (check) {
                newPar = str + combine;
                var updated = newPar.substring(0, newPar.length - 2);
                updated = updated + ".";
                console.log(updated)
              }
              //$(this).add('p');
              //newNode.append("This is a paragraph");
              //$(newNode).insertAfter($(this))
            }
          }
        })
      }
  }

})();
