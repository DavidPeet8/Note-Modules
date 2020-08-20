import { BrowserModule } from '@angular/platform-browser';
import { NgModule, SecurityContext } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';
import { MarkdownModule } from 'ngx-markdown';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CodeviewComponent } from './components/codeview/codeview.component';
import { DirectoryTreeComponent } from './components/directory-tree/directory-tree.component';
import { RenderParentComponent } from './components/render-parent/render-parent.component';
import { ServicesModule } from './services/services.module';

import { FetchRenderEventBusService } from '@services/fetch-render-event-bus.service';
import { FileAccessAPIService } from '@services/file-access-api.service';

import { MarkedOptions, MarkedRenderer } from 'ngx-markdown'

export function markedOptionsFactory(): MarkedOptions 
{
  const renderer = new MarkedRenderer();

  renderer.blockquote = (text:string) => 
  {
    return `<blockquote class="md-blockquote">${text}</blockquote>`;
  }

  renderer.heading = (text:string, level:number) => 
  {
    return `<h${level} class="md-h${level}">${text}</h${level}>`;
  }

  renderer.hr = () => 
  {
    return '<hr class="md-hr">';
  }

  renderer.list = (body:string, ordered:boolean, start:number) => 
  {
    let char = ordered ? 'o' : 'u'
    return `<${char}l start="${start}" class="md-${char}l">${body}</${char}l>`;
  }
  
  renderer.paragraph = (text:string) => 
  {
    return `<p class="md-p">${text}</p>`;
  }

  renderer.html = (html:string) => 
  {
    return `<section class="md-html">${html}</section>`;
  }

  renderer.listitem = (text:string) => 
  {
    return `<li class="md-li">${text}</li>`;
  }

  renderer.table = (header:string, body:string) => 
  {
    return `
    <table class="md-table">
      <thead>${header}</thead>
      ${body}
    </table>`;
  }

  renderer.codespan = (text:string) => 
  {
    return `<code class="md-codespan">${text}</code>`
  }

  renderer.strong = (text:string) => 
  {
    return `<strong class="md-strong">${text}</strong>`
  }

  return {
    renderer: renderer,
    gfm: true,
    breaks: false,
    pedantic: false,
    smartLists: true,
    smartypants: false,
  };
}

@NgModule({
  declarations: [
    AppComponent,
    CodeviewComponent,
    DirectoryTreeComponent,
    RenderParentComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MarkdownModule.forRoot({ 
      loader: HttpClient, 
      sanitize: SecurityContext.NONE, 
      markedOptions: 
      {
        provide: MarkedOptions, 
        useFactory: markedOptionsFactory
      }
    }),
    ServicesModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
