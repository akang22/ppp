import { Readability } from "@mozilla/readability";
import { readFileSync, writeFileSync } from "fs";
import { JSDOM } from "jsdom";

function main() {
    const args = process.argv;
    if (args.length < 3) {
        throw new Error(`parse_article: Less than 3 arguments passed: ${args}`);
    }
    const html_file = readFileSync(args[2], {encoding: "utf-8"}).trim();
    const html_document = new JSDOM(html_file).window.document;
    const ret = new Readability(html_document).parse();
    writeFileSync(`${args[2]}.json`, JSON.stringify(ret));
}

main();
