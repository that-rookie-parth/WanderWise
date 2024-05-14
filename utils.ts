import { writeFileSync } from "fs";
import { join } from "path";

export const fetchAllLinks = (data: string) => {
  const linkRegex = /<a\s+(?:[^>]*?\s+)?href=(["'])(.*?)\1/g;
  const links = new Set<string>();
  let match: RegExpExecArray | null;
  while ((match = linkRegex.exec(data)) !== null) {
    links.add(match[2]);
  }
  return Array.from(links)
    .filter((link) => link.startsWith("/"))
    .filter((link) => link.includes("/en/"));
};

export const storeData = (link: string, data: string) => {
  const temp = link.split("/");
  const name = temp.slice(temp.length - 3).join("-");
  console.log(`content/${name} written.`);
  writeFileSync(join(__dirname, "content", name), data, { encoding: "utf-8" });
};

export const delay = (s: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, s);
  });
