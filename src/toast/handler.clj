(ns toast.handler
  (:use compojure.core
        [clojure.string :only [split split-lines]]
        [ring.util.response :only [redirect]])
  (:require [compojure.handler :as handler]
            [compojure.route :as route]
            [clojure.java.io :as io]
            [net.cgrand.enlive-html :as html]))

(def add (html/html-resource "toast/add.html"))

(html/deftemplate index "toast/index.html" [books]
  [:li]
  (html/clone-for [book books] (html/content book)))

(html/deftemplate search-results "toast/search-results.html" [recipes]
  [:li]
  (html/clone-for [recipe recipes]
                  [:span.recipe] (html/content (:recipe recipe))
                  [:span.book] (html/content (:book recipe))))

(def book-root "./var/books")
(defn book-path [title] [book-root title])
(defn recipe-path [book recipe] (conj (book-path book) recipe))

(defn add-recipes [title recipes]
  (doseq [recipe recipes]
    (let [recipe-file (apply io/file (recipe-path title recipe))]
      (io/make-parents recipe-file)
      (spit recipe-file ""))))

(defn path-elems [path] (split path #"/"))
(defn files-below [root] (rest (file-seq (io/file root))))

(defn all-recipes []
  (letfn [(extract-info [file] (drop 3 (path-elems (.getPath file))))
          (recipe? [path] (= 2 (count path)))]
    (->> (files-below book-root)
         (map extract-info)
         (filter recipe?)
         (map #(array-map :book (first %) :recipe (second %))))))

(defn book-titles []
  (sort (distinct (map :book (all-recipes)))))

(defn search-recipes [substring]
  (letfn [(name-matches [recipe] (.contains (:recipe recipe) substring))]
    (filter name-matches (all-recipes))))

(defn valid-name [name]
  (re-find #"^[A-Za-z0-9- ]+$" name))

(defroutes app-routes
  (GET "/" [] (index (book-titles)))
  (GET "/add" [] (html/emit* add))
  (POST "/add" [title recipes]
        (let [recipe-list (split-lines recipes)]
          (if (every? valid-name (conj recipe-list title))
            (do (add-recipes title (split-lines recipes))
                (redirect "/"))
            "Sorry: unaccented letters, numbers, hyphens and spaces only.")))
  (GET "/search" [query]
       (search-results (search-recipes query)))
  (route/not-found "Not Found"))

(def app
  (handler/site app-routes))
