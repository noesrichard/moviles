import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { LoginPage } from './pages/login/login.page';
import { SignupPage } from './pages/signup/signup.page';

@NgModule({
  declarations: [LoginPage, SignupPage],
  imports: [CommonModule, AuthRoutingModule],
})
export class AuthModule {}
