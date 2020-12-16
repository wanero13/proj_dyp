import React, { Component } from 'react';
import {View, TouchableOpacity, Text, Button, StyleSheet, TextInput} from 'react-native';
import { Actions } from 'react-native-router-flux'
import AsyncStorage from "@react-native-community/async-storage";
import FlashMessage from "react-native-flash-message";


export default class Home extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount = async () => {
        this.willFocusSubscription = this.props.navigation.addListener(
            'willFocus',
            () => {
                this.isAuth()
            }
        );
    }

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    }

    isAuth = async () => {
        let cookie = await AsyncStorage.getItem('cookie');
        console.log(cookie);
        fetch("http://localhost:5000/api/login", {
            headers: {'Cookie': cookie},
            method: 'get',
            credentials: "include"
        }).then((response) => {
            return response;
        }).then((responseObject) => {
            console.log(responseObject.status);
            if (responseObject.status !== 200){
                Actions.newUser();
            }
        }).catch((error) => {
            console.log('error: ' + error);
            this.setState({logged: false});
        })}


    onSubmitLogout = async (event) => {
        event.preventDefault();
        let cookie = await AsyncStorage.getItem('cookie');
        fetch("http://localhost:5000/api/logout", {
            headers: {'Cookie': cookie},
            method: 'post',
            credentials: "include"
        }).then((response) => {
            if (!response.ok) {
                throw new Error(response.statusText);
            } else return response;
        }).then((responseObject) => {
            console.log("Logged out user")
            Actions.newUser();
        }).catch((error) => {
            console.log('error: ' + error);
        })
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.text}>Welcome!</Text>
                <TouchableOpacity style={styles.button} onPress={Actions.notes}>
                    <Text style={styles.buttonText}>Notes</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={Actions.pnotes}>
                    <Text style={styles.buttonText}>Private Notes</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={Actions.addnote}>
                    <Text style={styles.buttonText}>Add Note</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={Actions.changepasswd}>
                    <Text style={styles.buttonText}>Change Password</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={this.onSubmitLogout.bind(this)}>
                    <Text style={styles.buttonText}>Logout</Text>
                </TouchableOpacity>
            </View>
        )
    }
}
const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        backgroundColor: '#fefefe',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        fontSize: 30,
        color: '#000000',
        marginVertical: 50
    },
    button: {
        width: 260,
        backgroundColor: '#1520a6',
        borderRadius: 26,
        paddingVertical: 16,
        marginVertical:10,
    },
    buttonText: {
        fontWeight: '500',
        color: '#fff5e1',
        fontSize: 20,
        textAlign: 'center',
    }
});
