import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { User } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit() {}

  signin(username: string, password: string) {
    const user = { username: username, password: password };
    this.auth.signin(user).subscribe(res => { 
      localStorage.setItem("jwt", res.token)
      localStorage.setItem("userId", res.userId)
      localStorage.setItem("username", res.username)
      this.router.navigate(["/home"])
    });
  }
}
