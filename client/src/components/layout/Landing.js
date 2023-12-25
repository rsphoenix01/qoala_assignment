import React, { Component } from "react";
import { connect } from "react-redux";
import { authenticateUser } from "../../actions/auth";
import GoogleButton from "../ui/GoogleButton";

class Landing extends Component {
  componentDidMount = () => {
    if (this.props.auth.isAuthenticated) this.props.history.push("/dashboard");
    if (this.props.location.search.length > 0) {
      const code = this.getAuthCodeFromLocation(this.props.location.search);
      this.props.authenticateUser(code);
    }
  };

  getAuthCodeFromLocation = str => {
    return str.substring(6);
  };

  render() {
    return (
      <div className="landing full-height">
        <div className="dark-overlay landing-inner text-light">
          <div className="container">
            <div className="row">
              <div className="col-md-12 text-center">
                <h1 className="display-3 mb-5">FLASK-REACT Boilerplate</h1>
                <p className="lead">
                  {" "}
                  Get Started in not time with Python, Flask, React, Redux, and
                  more...
                </p>
                <hr
                  style={{
                    height: "2px",
                    backgroundColor: "#fff",
                    width: "40%",
                    margin: "5rem auto"
                  }}
                />
                <GoogleButton text="Login with Google" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const mapDispatchToProps = dispatch => ({
  authenticateUser: authCode => dispatch(authenticateUser(authCode))
});

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Landing);
