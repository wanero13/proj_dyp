import React, {Component} from 'react';
import {Router, Stack, Scene, ActionConst} from 'react-native-router-flux';

import Login from './components/Login';
import Signup from './components/Signup';
import Home from './components/Home'
import Notes from './components/Notes'
import PrivateNotes from './components/PrivateNotes'
import AddNote from './components/AddNote'
import Auth from "./components/Auth";
import ChangePasswd from "./components/ChangePasswd";

export default class Routes extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Router>
                <Stack key='root'>
                    <Scene key='newUser' hideNavBar={true}>
                        <Scene key='auth' component={Auth} title='Auth' initial={true}/>
                        <Scene key='login' component={Login} title='Login' />
                        <Scene key='signup' component={Signup} title='Register'/>
                    </Scene>
                    <Scene key='authUser' hideNavBar={true} type={ActionConst.RESET}>
                        <Scene key='home' component={Home} title='Home' type={ActionConst.RESET}/>
                        <Scene key='notes' component={Notes} title='Notes'/>
                        <Scene key='privatenotes' component={PrivateNotes} title='Privete notes'/>
                        <Scene key='addnote' component={AddNote} title='Add note'/>
                        <Scene key='changepasswd' component={ChangePasswd} title='Change password'/>
                    </Scene>
                </Stack>
            </Router>
        );
    }
}
