import axios from "axios";
import { delay, fetchAllLinks, storeData } from "./utils";
import { baseLink } from "./constants";
import { AsyncQueue } from "./async_queue";

async function main() {
  const baseLinks = [
    "/content/incredible-india-v2/en/destinations/states/maharashtra.html",
    "/content/incredible-india-v2/en/destinations/states/tamil-nadu.html",
    "/content/incredible-india-v2/en/destinations/states/uttar-pradesh.html",
    "/content/incredible-india-v2/en/destinations/states/karnataka.html",
    "/content/incredible-india-v2/en/destinations/states/andhra-pradesh.html",
    "/content/incredible-india-v2/en/destinations/states/delhi.html",
  ];

  const visited: Record<string, boolean> = {};

  const queue = new AsyncQueue();

  async function recurse(links: string[]) {
    if (links.length === 0) return;
    const link = links[0];
    if (link in visited && visited[link]) {
      links.shift();
      await delay(700);
      recurse(links);
    }

    queue.addLink(link);
    visited[link] = true;
    links.shift();
    await delay(700);
    recurse(links);
  }

  queue.fetchLink();
  recurse(baseLinks);
}

main();
