import { Injectable } from '@angular/core';
import * as katex from 'katex';
import * as marked from 'marked';

const katexOptions = {
  displayMode: false,
  throwOnError: false,
  macros: {
    "\\floor": "\\left\\lfloor{#1}\\right\\rfloor",
    "\\ceil": "\\left\lceil{#1}\\right\\rceil",
    "\\abs": "\\lvert{#1}\\rvert",
    "\\paren": "\\left({#1}\\right)",
    "\\brac": "\\left[{#1}\\right]",
    "\\brace": "\\lbrace{#1}\\rbrace",
    "\\angle": "\\langle{#1\\rangle",
    "\\group": "\\lgroup{#1}\\rgroup",
    "\\mn": "\\mathnormal{#1}",
    "\\reg": "\\text{\\textdollar}{#1}",
    "\\dlr": "\\text{\\textdollar}",
    "\\iff": "\\longleftrightarrow",
    "\\Iff": "\\Longleftrightarrow",
  }
};

class CustomRenderer extends marked.Renderer {
  blockquote(text: string) {
    return `<blockquote class="md-blockquote">${text}</blockquote>`;
  }

  heading(text: string, level: number) {
    const escapedText = text.toLowerCase().trim().replace(/[^\w]+/g, '-');

    return `
            <h${level} class="md-header md-h${level}">
              <a name="${escapedText}" class="anchor" href="#${escapedText}">
                <span class="header-link"></span>
              </a>
              ${text}
            </h${level}>`;
  }

  hr() {
    return '<hr class="md-hr">';
  }

  list(body: string, ordered: boolean, start: number) {
    let char = ordered ? 'o' : 'u'
    return `<${char}l start="${start}" class="md-${char}l">${body}</${char}l>`;
  }

  paragraph(text: string) {
    return `<p class="md-plaintext md-p">${text}</p>`;
  }

  html(html: string) {
    return `<section class="md-html">${html}</section>`;
  }

  listitem(text: string) {
    return `<li class="md-plaintext md-li">${text}</li>`;
  }

  table(header: string, body: string) {
    return `
    <table class="md-table">
      <thead>${header}</thead>
      ${body}
    </table>`;
  }

  codespan(text: string) {
    return `<code class="md-codespan">${text}</code>`
  }

  strong(text: string) {
    return `<strong class="md-plaintext md-strong">${text}</strong>`
  }

  em(text: string) {
    return `<em class="md-plaintext md-em">${text}</em>`;
  }
}

class CustomTokenizer extends marked.Tokenizer {
  codespan(src: string) {
    const match = matchTex(src);
    if (match.matched) {
      return match.data;
    }
    return marked.Tokenizer.prototype.codespan.call(this, src); // use original codespan tokenizer
  }
}

function matchTex(src: string) {
  const match = src.match(/(\$([^\$\n]+)\$|\$\$([^\$\n]+)\$\$)/);

  if (match) {
    let displayMode = match[0].startsWith("$$");
    katexOptions.displayMode = displayMode;
    let tex = katex.renderToString(match[0].substring(1, match[0].length - 1), katexOptions);

    return {
      matched: true,
      data: {
        type: 'html',
        raw: tex,
        text: tex
      }
    }
  }

  return { matched: false }
}

function getMarkedOptions(): Object {
  return {
    renderer: new CustomRenderer(),
    gfm: true,
    breaks: false,
    pedantic: false,
    smartLists: true,
    smartypants: false,
    tokenizer: new CustomTokenizer()
  };
}

// ------------------------------ SERVICE IMPLEMENTATION -------------------------------

@Injectable({
  providedIn: 'root'
})
export class Renderer {

  constructor() {
    // configure the marked renderer
    marked.setOptions(getMarkedOptions());
  }

  renderToString(code: string): string {
    let data = marked(code);
    return data;
  }
}
