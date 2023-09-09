"use strict"

const r = 32

function set_attributes(on, attrs) {
	for (const key in attrs)
		on.setAttribute(key, attrs[key])
}

function create_svg(tag, attrs, content) {
	let e = document.createElementNS("http://www.w3.org/2000/svg", tag)
	set_attributes(e, attrs)
	if (content)
		e.textContent = content
	return e
}

class PersonImage {
	constructor(pos, props) {
		this.pos = pos
		this.type = props.type
		this.title = props.title
		this.root = create_svg("g", {
			"class": [this.type, "person", "grabbable"].join(" "),
			transform: `translate(${pos.x} ${pos.y})`,
		})
		this.root.appendChild(create_svg("circle", {	r: 36}))
		this.root.appendChild(create_svg("text", {}, this.title[0]))
		this.root.appendChild(create_svg("title", {}, this.title))
	}
}

class Person extends PersonImage {
	constructor(pos, props) {
		super(pos, props)
		this.root.addEventListener("mousedown", this.on_mousedown.bind(this))
	}

	on_mousedown(e) {
		if (e.buttons != 1)
			return;
		e.preventDefault()
		dragger.start(e, this)
	}

	#chair
	get chair() { return this.#chair }
	set chair(chair) {
		if (this.#chair)
			this.#chair.person = null
		this.#chair = chair
		if (this.#chair)
			this.#chair.person = this
		recalc_answer()
	}
}

class PersonSource extends PersonImage {
	constructor(pos, props) {
		super(pos, props)
		this.props = props
		this.root.addEventListener("mousedown", this.on_mousedown.bind(this))
		layer_ui.appendChild(this.root)
	}

	on_mousedown(e) {
		if (e.buttons != 1)
			return;
		e.preventDefault()
		let person = new Person(this.pos, this.props)
		dragger.start(e, person)
	}
}

class Chair {
	#root

	constructor(parent, x, y) {
		this.#root = create_svg("circle", {
			"class": "chair",
			r: r,
			cx: x,
			cy: y,
		})
		this.pos = {x, y}
		this.#root.chair = this
		parent.appendChild(this.#root)
	}

	#person
	get person() { return this.#person }
	set person(person) {
		if (this.#person)
			layer_persons.removeChild(this.#person.root)
		this.#person = person
		if (this.#person)
			layer_persons.appendChild(this.#person.root)
	}
}

class Dragger {
	#object
	#chair
	#offset
	#transform

	get #root() { return this.#object.root }

	constructor() {
		document.body.addEventListener("mousemove", this.#move.bind(this))
		document.body.addEventListener("mouseleave", this.#finish.bind(this))
		document.body.addEventListener("mouseup", this.#finish.bind(this))
	}

	start(e, person) {
		this.#object = person
		this.#object.chair = null
		this.#offset = Dragger.get_mouse_position(e)

		let transforms = this.#root.transform.baseVal;
		if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
			this.#transform = playground.createSVGTransform();
			this.#transform.setTranslate(0, 0);
			transforms.baseVal.insertItemBefore(this.#transform, 0);
		} else {
			this.#transform = transforms.getItem(0);
			this.#offset.x -= this.#transform.matrix.e;
			this.#offset.y -= this.#transform.matrix.f;
		}

		layer_dnd.appendChild(this.#root)
		this.#move(e)
	}

	#move(e) {
		if (!this.#object)
			return

		e.preventDefault()

		let chair = Dragger.find_chair(e.x, e.y)
		if (chair && this.#chair == chair)
			return
		this.#chair = chair
		if (chair) {
			let {x, y} = chair.pos
			this.#transform.setTranslate(x, y)
		} else {
			let coord = Dragger.get_mouse_position(e);
			this.#transform.setTranslate(coord.x - this.#offset.x, coord.y - this.#offset.y);
		}
	}

	#finish(e) {
		if (!this.#object)
			return

		e.preventDefault()

		layer_dnd.removeChild(this.#root)
		this.#object.chair = this.#chair
		this.#object = null
	}

	static find_chair(x, y) {
		let elms = document.elementsFromPoint(x, y)
		for (let elm of elms) {
			if (elm.chair)
				return elm.chair
		}
		return null
	}

	static get_mouse_position(e) {
		let CTM = layer_dnd.getScreenCTM()
		return {
			x: (e.clientX - CTM.e) / CTM.a,
			y: (e.clientY - CTM.f) / CTM.d
		}
	}
}

const type_map = {
	liar: "L",
	truthful: "T",
	sly: "S",
	undefined: "",
}

function recalc_answer() {
	let answer = chairs.map((chair) => type_map[chair.person?.type]).join("")
	// answer.value = chairs.map((chair) => type_map[chair.person?.type]).join("")
}

let dragger, chairs

document.addEventListener("DOMContentLoaded", (e) => {
	dragger = new Dragger()

	new PersonSource({x: sidebar_x + 48, y: sidebar_y + 1 * 48}, {type: "liar", title: "Лжец"})
	new PersonSource({x: sidebar_x + 48, y: sidebar_y + 3 * 48}, {type: "truthful", title: "Правдолюб"})
	new PersonSource({x: sidebar_x + 48, y: sidebar_y + 5 * 48}, {type: "sly", title: "Хитрец"})

	set_attributes(playground, {
		viewBox: `0 0 ${3*R_outer} ${2*R_outer}`,
		width: `${3*R_outer}px`,
		height: `${2*R_outer}px`,
	})

	layer_table.appendChild(create_svg("circle", {
		"class": "table",
		r: R_table,
		cx: table_x,
		cy: table_y,
	}))

	chairs = []
	for (let k = 0; k < N; k++) {
		let phi = 2 * Math.PI * k / N
		chairs[k] = new Chair(layer_table, table_x + R * Math.cos(phi), table_y + R * Math.sin(phi))
	}
})
