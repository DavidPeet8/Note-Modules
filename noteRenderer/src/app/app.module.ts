import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';
import { MarkdownModule } from 'ngx-markdown';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CodeviewComponent } from './components/codeview/codeview.component';
import { DirectoryTreeComponent } from './components/directory-tree/directory-tree.component';
import { RenderParentComponent } from './components/render-parent/render-parent.component';

@NgModule({
  declarations: [
    AppComponent,
    CodeviewComponent,
    DirectoryTreeComponent,
    RenderParentComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MarkdownModule.forRoot({ loader: HttpClient }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
