(ns toast.handler
  (:use compojure.core
        [clojure.string :only [split-lines]]
        [ring.util.response :only [redirect]])
  (:require [compojure.handler :as handler]
            [compojure.route :as route]
            [clojure.java.io :as io]
            [net.cgrand.enlive-html :as html]))

(def add (html/html-resource "toast/add.html"))

(html/deftemplate index "toast/index.html" [books]
  [:ul]
  (html/clone-for [book books] (html/content book)))

(def book-root "./var/books")
(defn book-path [title] [book-root title])
(defn recipe-path [book recipe] (conj (book-path book) recipe))

(defn add-recipes [title recipes]
  (doseq [recipe recipes]
    (let [recipe-file (apply io/file (recipe-path title recipe))]
      (io/make-parents recipe-file)
      (spit recipe-file ""))))

(defn book-titles []
  (.list (io/file book-root)))

(defroutes app-routes
  (GET "/" [] (index (book-titles)))
  (GET "/add" [] (html/emit* add))
  (POST "/add" [title recipes]
        (add-recipes title (split-lines recipes))
        (redirect "/"))
  (route/not-found "Not Found"))

(def app
  (handler/site app-routes))
