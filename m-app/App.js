import React, {Component} from 'react';
import {StyleSheet, Text, View} from 'react-native';
import Routes from "./src/Routes";
import AsyncStorage from '@react-native-community/async-storage'

const cookie = ''

export default class App extends Component {

    setCurrentUser = (id, user) => {
        this.setState({userId: id, currentUser: user});
    };

    setTokens = (authToken, refreshToken) => {
        this.setState({authToken: authToken, refreshToken: refreshToken});
    };

    render() {
        return (
            <View style={styles.container}>
                <Routes/>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        backgroundColor: '#fefefe',
        justifyContent: 'center',
    },
});
