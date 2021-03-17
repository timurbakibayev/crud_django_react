'use strict';
const e = React.createElement;

class MyReactApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    swal("Hello world!");

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(e(MyReactApp), domContainer);
