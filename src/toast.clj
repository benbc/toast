(ns toast
  (:use compojure.core
        ring.adapter.jetty ring.util.response
        hiccup.core hiccup.form-helpers hiccup.page-helpers)
  (:gen-class))

(def state (atom {:books '("Real Fast Food", "Head to Tail Eating")
                  :recipes '()}))

(defn books [] (get @state :books))
(defn recipes [] (get @state :recipes))
(defn add-recipe-to-state [state book name]
  (assoc state :recipes (cons {:book book :name name} (get state :recipes))))
(defn add-recipe
  [book name] (swap! state add-recipe-to-state book name))
(defn recipe-book [recipe] (get recipe :book))

(defn add [xs x]
  (cons x xs))

(defn error-404 [body]
  {:status 404, :body body})

(defroutes main-routes
  (GET "/" []
       (swap! state add :foo)
       (html [:h1 "Here is the thing"] [:p @state]))
  (GET "/recipes/add" []
       (html (form-to [:post "/recipes/add"]
                      (drop-down "book" (books)) [:br]
                      "Name:" (text-field "name") [:br]
                      (submit-button "add"))))
  (POST "/recipes/add" [book name]
        (add-recipe book name)
        (redirect "/recipes/list"))
  (GET "/recipes/list" []
       (html (unordered-list (map recipe-book (recipes)))))
  (ANY "*" []
       (error-404 (html [:h1 "Doh!"]))))

(defn -main [& args]
  (run-jetty main-routes {:port 8080}))
