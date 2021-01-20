import React, {Component} from 'react';
import {View, TouchableOpacity, Text, Button, StyleSheet, TextInput, FlatList} from 'react-native';
import {Actions} from 'react-native-router-flux';


export default class PrivateNotes extends Component {
    constructor(props) {
        super(props);
        this.state = {
            notes: [],
        };
    }

    componentDidMount = async () => {
        this.willFocusSubscription = this.props.navigation.addListener(
            'willFocus',
            async() => {
                await this.loadNotes();
            }
        );

    };

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    };

    loadNotes = async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/pnotes`, {
                method: 'GET',
                credentials: "include",
            });
            console.log(data);
            var data = await response.json();
            this.setState({notes: data})
        } catch (error) {
            console.log(error);
        }
    };



    render() {
        let startList = <Text>There are no private notes.</Text>;
        if (this.state.notes.length > 0) {
            startList = <FlatList
                data={this.state.notes}
                renderItem={({item}) => (
                    <View style={styles.container}>
                        <TouchableOpacity style={styles.button} onPress={() => Actions.note({note_id: item[0]})}>
                            <Text style={styles.buttonText}>
                                {item[1].toString()}
                            </Text>
                        </TouchableOpacity>
                    </View>)}
                keyExtractor={item => item.toString()}
                extraData={this.state}
            />
        }
        return (
            <View style={styles.container}>
                <Text style={styles.logoText}>Private Notes</Text>
                {startList}
            </View>
        )
    }
}
const styles = StyleSheet.create({
    logoText: {
        marginVertical: 100,
        fontSize: 30,
        color: '#000000',
    },
    container: {
        flex: 1,
        backgroundColor: '#fefefe',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        flexGrow: 1,
        fontSize: 20,
        color: '#000000'
    },
    button: {
        width: 300,
        backgroundColor: '#1520a6',
        borderRadius: 26,
        paddingVertical: 16,
        marginVertical: 10,
        color: '#ffffff'
    },
    buttonText: {
        fontWeight: '500',
        color: '#000000',
        fontSize: 20,
        textAlign: 'center',
    },
    addButton: {
        width: 160,
        backgroundColor: '#000000',
        borderRadius: 20,
        paddingVertical: 10,
        marginVertical: 10,
        color: '#ffffff',
        textAlign: 'center'
    },
    addText: {
        color: '#ffffff',
        fontSize: 20,
        textAlign: 'center',
    },
    inputBox: {
        width: 320,
        backgroundColor: '#102030',
        fontSize: 16,
        borderRadius: 20,
        paddingHorizontal: 10,
        marginVertical: 12,
        height: 50,
        color: '#ffffff'
    },
});
