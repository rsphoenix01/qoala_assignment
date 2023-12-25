import React from "react";

/*
    @component      GoogleButton
    @desc           Displays Google login/signup button
    @input          text
*/

const GoogleButton = ({ text }) => {
  const login = () => {
    console.log(login);
  };
  return (
    <div style={{ textAlign: "center" }}>
      <div id="signinButton" className="text-center ">
        <span
          className="g-signin"
          data-scope="openid email profile"
          data-clientid="878062137643-sa1a39td912mms0qbqbou77jolpcnrjk.apps.googleusercontent.com"
          data-redirecturi="postmessage"
          data-accesstype="offline"
          data-cookiepolicy="single_host_origin"
          data-callback="login"
          data-approvalprompt="force"
        >
          <button
            className="btn google-custom btn btn-lg loginBtn btn loginBtn loginBtn--google"
            type="button"
          >
            {text}
          </button>
        </span>
      </div>
    </div>
  );
};

export default GoogleButton;
