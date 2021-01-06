import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CodeviewComponent } from './components/codeview/codeview.component';
import { DirectoryTreeComponent } from './components/directory-tree/directory-tree.component';
import { RenderParentComponent } from './components/render-parent/render-parent.component';
import { ServicesModule } from './services/services.module';

import { HelpModalComponent } from './components/help-modal/help-modal.component';
import { SearchBarComponent } from './components/search-bar/search-bar.component';
import { InstallModalComponent } from './components/install-modal/install-modal.component'

@NgModule({
  declarations: [
    AppComponent,
    CodeviewComponent,
    DirectoryTreeComponent,
    RenderParentComponent,
    HelpModalComponent,
    SearchBarComponent,
    InstallModalComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ServicesModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
