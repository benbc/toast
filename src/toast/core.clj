(ns toast.core
  (:require [noir.server :as server]
            [noir.core :refer [defpage defpartial]]))

(defpage "/welcome" []
  "Welcome to Noir!")

(server/start 8080)
