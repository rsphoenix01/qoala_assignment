import React from "react";

const Footer = () => {
  return (
    <footer
      className="bg-dark text-white p-4 text-center"
      style={{ position: "relative" }}
    >
      <h3>
        <small>Copyright &copy; {new Date().getFullYear()}</small> FLASK-REACT{" "}
        <small>Boilerplate</small>
      </h3>
    </footer>
  );
};

export default Footer;
