import React from "react";
import ReactDOM from 'react-dom/client'
import './index.css'


class ShoppingList extends React.Component {
    render() {
        return (
            <div className="shopping-list">
                <h1>Lista de compras para {this.props.name}</h1>
                <ul>
                    <li>Instagram</li>
                    <li>WhatsApp</li>
                    <li>Oculus</li>
                </ul>
            </div>
        );
    }
}

class Board extends React.Component {
    renderSquare(i) {
        return <Square value={i}/>;
    }
}

class Square extends React.Component {
    render() {
        return (
            <button className="Square">
                {this.props.value}
            </button>
        );
    }
}


alert('Hello World!');
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShoppingList/>);
// root.render(<Board/>)