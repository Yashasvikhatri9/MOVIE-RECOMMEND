const User = require("../models/User");

exports.getProfile = async (req, res) => {
  const user = await User.findById(req.user);
  res.json(user);
};

exports.updateProfile = async (req, res) => {
  const { name, interests, profilePic } = req.body;
  const updatedUser = await User.findByIdAndUpdate(
    req.user,
    { name, interests, profilePic },
    { new: true }
  );
  res.json(updatedUser);
};
