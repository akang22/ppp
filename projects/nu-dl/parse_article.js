import { Readability } from "@mozilla/readability";
import { readFileSync, writeFileSync } from "fs";
import jsdom, { JSDOM } from "jsdom";

async function main() {
    const args = process.argv;
    if (args.length < 3) {
        throw new Error(`parse_article: Less than 3 arguments passed: ${args}`);
    }
    const virtualConsole = new jsdom.VirtualConsole();
    virtualConsole.on("error", () => {
        // throw away all errors.
        // yeah this is pretty bad. I think they have poor css support (which doeesn't matter imo)
        // when i port to python i'll get rid of all js/css after render.
    });
    const html_document = (await JSDOM.fromFile(args[2], { virtualConsole })).window.document;
    const u_html_content = new Readability(html_document).parse().textContent.trim();
    const decoded_string = JSON.parse('"' + u_html_content.replace(/([^\\]|^)\\x/g, '$1\\u00') + '"');
    writeFileSync(`${args[2]}.json`, JSON.stringify(decoded_string), {encoding: "utf8"});
}

await main();
