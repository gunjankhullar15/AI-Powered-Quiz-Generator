import { Routes } from '@angular/router';
import { AuthGuard } from './Core/Guards/auth-guard';
import { Testhistory } from './Features/Components/Test-History/pages/testhistory/testhistory';
import { Login } from './Features/Components/Login/pages/login/login';
import { Candidateinfo } from './Features/Components/Candidate-Info/pages/candidateinfo/candidateinfo';
import { Createtest } from './Features/Components/Create-Test/pages/createtest/createtest';
import { Result } from './Features/Components/Result/Pages/result/result';
import { Instructions } from './Features/Components/Instructions/pages/instruction/instruction';
import { TestPage } from './Features/Components/TestPage/pages/test-page/test-page';
import { TestPage1 } from './Features/Components/TestPage1/pages/test-page1/test-page1';
import { LoginGuard } from './Core/Guards/login-guard';



export const routes: Routes = [
  
    {path: '', redirectTo: 'login', pathMatch: 'full'},
 
    {path:'login',component:Login,canActivate: [LoginGuard]},
    
    {path:'history',component:Testhistory, canActivate: [AuthGuard]},

    {path:'candidateinfo',component:Candidateinfo, canActivate: [AuthGuard]},

    {path:'test',component:Createtest},

    {path: 'candidate/:testId',component: Candidateinfo,canActivate: [AuthGuard]},

    {path:'test-results',component:Result},

{
  path: 'inst/:testId',
  component: Instructions,canActivate: [AuthGuard]
},

// {
//     path: 'dummy',
//     component:Dummy,canActivate: [AuthGuard]
//   }
    
{path:'test1',component:TestPage, canActivate: [AuthGuard]},

{path:'test2',component:TestPage1, canActivate: [AuthGuard]},

];

