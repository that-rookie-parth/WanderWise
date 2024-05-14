import axios from "axios";
import { delay, fetchAllLinks, storeData } from "./utils";
import { baseLink } from "./constants";

export class AsyncQueue {
  links: string[] = [];
  visited: Record<string, boolean> = {};
  fetching = false;

  constructor() {}

  addLink(link: string) {
    this.links.push(link);
    // this.fetchLink();
  }

  async fetchLink() {
    if (this.fetching) return;
    if (this.links.length === 0) return;
    const link = this.links[0];
    if (link in this.visited && this.visited[link]) {
      this.links.shift();
      await delay(300);
      this.fetchLink();
    }

    this.fetching = true;
    const resp = await axios.get(baseLink + link);
    storeData(link, resp.data);
    const new_links = fetchAllLinks(resp.data);
    this.visited[link] = true;

    console.log(`visited.length: ${Object.keys(this.visited).length}`);

    this.links = [...this.links, ...new_links];
    await delay(700);
    this.fetching = false;
    this.links.shift();
    this.fetchLink();
  }
}
