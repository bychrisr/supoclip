import * as React from "react"
import { describe, expect, it } from "vitest"

import { render, screen } from "@testing-library/react"
import Link from "next/link"

import { Button } from "@/components/ui/button"

describe("<Button />", () => {
  it("renders a native button by default", () => {
    render(<Button>Click</Button>)
    expect(screen.getByRole("button", { name: "Click" })).toBeInTheDocument()
  })

  it("supports asChild rendering", () => {
    render(
      <Button asChild>
        <Link href="/x">Go</Link>
      </Button>
    )

    const link = screen.getByRole("link", { name: "Go" })
    expect(link.tagName).toBe("A")
  })

  it("applies variant classes", () => {
    render(<Button variant="destructive">Delete</Button>)
    const btn = screen.getByRole("button", { name: "Delete" })
    expect(btn.className).toContain("bg-destructive")
  })
})

