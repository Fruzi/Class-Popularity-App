package rawnsangels.bgu.application

import io.realm.RealmObject
import io.realm.annotations.PrimaryKey

open class Course(@PrimaryKey var courseId: Int = 0,
                  var departmentId: Int = 0,
                  var name: String = "") : RealmObject()
