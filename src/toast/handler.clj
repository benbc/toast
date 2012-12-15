(ns toast.handler
  (:use compojure.core
        [net.cgrand.enlive-html :only [html-resource emit*]])
  (:require [compojure.handler :as handler]
            [compojure.route :as route]))

(def index (html-resource "toast/index.html"))
(def add (html-resource "toast/add.html"))

(defroutes app-routes
  (GET "/" [] (emit* index))
  (GET "/add" [] (emit* add))
  (route/not-found "Not Found"))

(def app
  (handler/site app-routes))
