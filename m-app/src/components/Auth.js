import React, {Component} from 'react';
import {StyleSheet, Text, View, TouchableOpacity, TextInput} from 'react-native';
import {Actions} from 'react-native-router-flux'
import AsyncStorage from '@react-native-community/async-storage'
import CookieManager from 'react-native-cookies'

export default class Auth extends Component {
    componentDidMount() {
        this.isAuth();
    }

    isAuth = async () => {
        let cookie = await AsyncStorage.getItem('sId')
        fetch("http://localhost:5000/api/login", {
            headers: {'Cookie': cookie},
            method: 'get',
            credentials: "include"
        }).then((response) => {
            return response;
        }).then((responseObject) => {
            console.log(responseObject.status);
            if (responseObject.status === 200){
                Actions.authUser();
            }

            AsyncStorage.setItem('sId', responseObject.headers.get('set-cookie'))
            Actions.login()
        }).catch((error) => {
            console.log('error: ' + error);
            this.setState({logged: false});
        })
    };

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.text}>LOADING...</Text>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        marginVertical: 100,
        fontSize: 30,
        color: '#000000',
    },
});
