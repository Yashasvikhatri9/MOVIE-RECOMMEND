const Movie = require("../models/Movie");

exports.getAllMovies = async (req, res) => {
  const movies = await Movie.find();
  res.json(movies);
};

exports.getMovieById = async (req, res) => {
  const movie = await Movie.findById(req.params.id);
  res.json(movie);
};

exports.searchMovies = async (req, res) => {
  const { query } = req.query;
  const movies = await Movie.find({ title: { $regex: query, $options: "i" } });
  res.json(movies);
};
