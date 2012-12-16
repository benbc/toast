(ns toast.handler
  (:use compojure.core
        [net.cgrand.enlive-html :only [html-resource emit*]]
        [clojure.string :only [split-lines]]
        [ring.util.response :only [redirect]])
  (:require [compojure.handler :as handler]
            [compojure.route :as route]
            [clojure.java.io :as io]))

(def index (html-resource "toast/index.html"))
(def add (html-resource "toast/add.html"))

(def book-root "./var/books")
(defn book-path [title] [book-root title])
(defn recipe-path [book recipe] (conj (book-path book) recipe))

(defn add-recipes [title recipes]
  (doseq [recipe recipes]
    (let [recipe-file (apply io/file (recipe-path title recipe))]
      (io/make-parents recipe-file)
      (spit recipe-file ""))))

(defroutes app-routes
  (GET "/" [] (emit* index))
  (GET "/add" [] (emit* add))
  (POST "/add" [title recipes]
        (add-recipes title (split-lines recipes))
        (redirect "/"))
  (route/not-found "Not Found"))

(def app
  (handler/site app-routes))
