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
    MarkdownModule.forRoot({ loader: HttpClient, sanitize: SecurityContext.NONE }),
    ServicesModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
